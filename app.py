import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="Standard Node UX")

st.title("🎮 표준 노드 에디터 인터렉션")
st.markdown("""
* **연결 수정**: 노드 입구(Input)에 연결된 선의 끝점을 드래그하여 다른 노드로 옮길 수 있습니다.
* **선택 및 삭제**: 노드나 선을 클릭하여 선택한 후, 키보드의 **Delete** 또는 **Backspace** 키를 눌러 삭제하세요.
* **노드 추가**: 빈 화면 우클릭
""")

node_editor_code = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; background-color: #1a1a1a; overflow: hidden; }
        #rete { height: 100vh; width: 100vw; }
        
        /* 연결선 기본 스타일 */
        .connection .main-path {
            stroke: #666;
            stroke-width: 3px !important;
            transition: all 0.2s;
        }

        /* 선이 선택되었을 때 (표준 방식) */
        .connection.selected .main-path {
            stroke: #ff9d00 !important;
            stroke-width: 5px !important;
            filter: drop-shadow(0 0 5px #ff9d00);
        }

        .node { background: #222 !important; border: 1px solid #444 !important; }
        .node.selected { border: 2px solid #ff9d00 !important; }
    </style>
</head>
<body>
    <div id="rete"></div>

    <script src="https://cdn.jsdelivr.net/npm/vue@2.6.14/dist/vue.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/rete@1.4.5/build/rete.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/rete-vue-render-plugin@0.5.0/build/vue-render-plugin.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/rete-connection-plugin@0.9.0/build/connection-plugin.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/rete-context-menu-plugin@0.5.2/build/context-menu-plugin.min.js"></script>

    <script>
        const numSocket = new Rete.Socket('Data');

        class BlueNode extends Rete.Component {
            constructor() { super("Logic Node"); }
            builder(node) {
                return node
                    .addInput(new Rete.Input('in', "In", numSocket))
                    .addOutput(new Rete.Output('out', "Out", numSocket));
            }
        }

        async function init() {
            const container = document.querySelector('#rete');
            const editor = new Rete.NodeEditor('demo@0.1.0', container);
            
            // connection-plugin의 기본 인터렉션(드래그 수정 등)을 활성화
            editor.use(ConnectionPlugin.default, { 
                curvature: 0.4,
                interactive: true // 선을 마우스로 조작 가능하게 설정
            }); 
            editor.use(VueRenderPlugin.default);
            editor.use(ContextMenuPlugin.default);

            const component = new BlueNode();
            editor.register(component);

            const n1 = await component.createNode({x: 100, y: 150});
            const n2 = await component.createNode({x: 500, y: 150});
            editor.addNode(n1);
            editor.addNode(n2);
            editor.connect(n1.outputs.get('out'), n2.inputs.get('in'));

            // 키보드 삭제 이벤트 바인딩 (표준 방식)
            window.addEventListener('keydown', e => {
                if (e.key === 'Delete' || e.key === 'Backspace') {
                    // 선택된 노드 삭제
                    editor.selected.each(n => editor.removeNode(n));
                    // 선택된 연결선 삭제
                    editor.trigger('multiselectnode', { node: null, accumulate: false }); // 선택 해제 유도
                    // Rete.js는 기본적으로 선택된 요소를 저장하므로 이를 활용하여 삭제 로직이 작동합니다.
                }
            });

            editor.view.resize();
        }

        window.onload = init;
    </script>
</body>
</html>
"""

components.html(node_editor_code, height=750, scrolling=False)
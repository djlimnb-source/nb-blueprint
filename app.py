import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="Blueprint UX")

st.title("🎮 블루프린트 인터렉션 체험")
st.caption("연결선을 클릭하면 즉시 삭제됩니다. 노드를 드래그하여 위치를 수정하세요.")

# HTML/JavaScript 코드를 변수에 담습니다.
node_editor_code = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; background-color: #1a1a1a; overflow: hidden; }
        #rete { height: 100vh; width: 100vw; }
        
        /* 연결선 UX 스타일 */
        .connection .main-path {
            stroke: #888;
            stroke-width: 4px !important;
            transition: all 0.2s;
            cursor: pointer;
        }
        .connection:hover .main-path {
            stroke: #ff9d00 !important;
            filter: drop-shadow(0 0 8px #ff9d00);
        }

        /* 노드 디자인 */
        .node { background: #222 !important; border: 1px solid #444 !important; border-radius: 5px !important; }
        .node.selected { border: 2px solid #ff9d00 !important; }
        .node .title { background: #333 !important; color: white !important; font-size: 13px !important; padding: 8px !important; }
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
            constructor() { super("Node"); }
            builder(node) {
                return node
                    .addInput(new Rete.Input('in', "In", numSocket))
                    .addOutput(new Rete.Output('out', "Out", numSocket));
            }
        }

        async function init() {
            const container = document.querySelector('#rete');
            const editor = new Rete.NodeEditor('demo@0.1.0', container);
            
            editor.use(ConnectionPlugin.default, { curvature: 0.4 }); 
            editor.use(VueRenderPlugin.default);
            editor.use(ContextMenuPlugin.default);

            const component = new BlueNode();
            editor.register(component);

            // 초기 노드 배치
            const n1 = await component.createNode({x: 50, y: 150});
            const n2 = await component.createNode({x: 400, y: 150});
            editor.addNode(n1);
            editor.addNode(n2);
            editor.connect(n1.outputs.get('out'), n2.inputs.get('in'));

            // [핵심] 연결선 클릭 시 삭제 인터렉션
            editor.on('connectionpick', (connection) => {
                editor.removeConnection(connection);
                return false; // 기본 픽 동작 방지
            });

            editor.view.resize();
        }

        window.onload = init;
    </script>
</body>
</html>
"""

# Streamlit 컴포넌트로 실행
components.html(node_editor_code, height=700, scrolling=False)
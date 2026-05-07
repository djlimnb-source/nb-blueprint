import streamlit as st
import streamlit.components.v1 as components
import base64

st.set_page_config(layout="wide", page_title="Blueprint Final")

st.title("🎮 블루프린트 에디터 (최종 수정본)")
st.info("1. 선을 클릭하면 주황색으로 강조됩니다. 2. 그 상태에서 Delete 키를 눌러 삭제하세요.")

# HTML/JS 코드를 안전하게 전달하기 위한 설정
raw_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; background-color: #1a1a1a; overflow: hidden; font-family: sans-serif; }
        #rete { height: 100vh; width: 100vw; }
        .connection .main-path { stroke: #666; stroke-width: 5px !important; transition: all 0.2s; cursor: pointer; fill: none; }
        .connection.selected .main-path { stroke: #ff9d00 !important; filter: drop-shadow(0 0 8px #ff9d00); stroke-width: 7px !important; }
        .node { background: #252525 !important; border: 1px solid #444 !important; border-radius: 8px !important; min-width: 160px !important; }
        .node.selected { border: 2px solid #ff9d00 !important; }
        .node .title { background: #333 !important; color: #eee !important; padding: 10px !important; font-size: 14px; }
        .socket { width: 20px !important; height: 20px !important; margin: 6px !important; background: #777 !important; }
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
                return node.addInput(new Rete.Input('in', "Input", numSocket))
                           .addOutput(new Rete.Output('out', "Output", numSocket));
            }
        }

        async function init() {
            const container = document.querySelector('#rete');
            const editor = new Rete.NodeEditor('demo@0.1.0', container);
            editor.use(ConnectionPlugin.default, { curvature: 0.4, interactive: true });
            editor.use(VueRenderPlugin.default);
            editor.use(ContextMenuPlugin.default);

            const component = new BlueNode();
            editor.register(component);

            // 노드 3개를 겹치지 않게 넓게 배치 (X: 100, 500, 900 / Y: 100, 400, 100)
            const n1 = await component.createNode({ x: 100, y: 100 });
            const n2 = await component.createNode({ x: 500, y: 400 });
            const n3 = await component.createNode({ x: 900, y: 100 });

            editor.addNode(n1); editor.addNode(n2); editor.addNode(n3);
            editor.connect(n1.outputs.get('out'), n2.inputs.get('in'));
            editor.connect(n2.outputs.get('out'), n3.inputs.get('in'));

            let selectedConn = null;

            // 선 클릭 감지 및 클래스 부여
            editor.on('connectionpick', (c) => {
                if (selectedConn) {
                    const prev = editor.view.connections.get(selectedConn);
                    if(prev) prev.el.classList.remove('selected');
                }
                selectedConn = c;
                const curr = editor.view.connections.get(c);
                if(curr) curr.el.classList.add('selected');
                return true;
            });

            // 배경 클릭 시 선택 해제
            editor.on('click', () => {
                if (selectedConn) {
                    const v = editor.view.connections.get(selectedConn);
                    if(v) v.el.classList.remove('selected');
                    selectedConn = null;
                }
            });

            // Delete 키로 삭제
            window.addEventListener('keydown', e => {
                if (e.key === 'Delete' || e.key === 'Backspace') {
                    editor.selected.each(n => editor.removeNode(n));
                    if (selectedConn) {
                        editor.removeConnection(selectedConn);
                        selectedConn = null;
                    }
                }
            });
            editor.view.resize();
        }
        window.onload = init;
    </script>
</body>
</html>
"""

# HTML을 Base64로 인코딩하여 파이썬 구문 에러 방지
b64_html = base64.b64encode(raw_html.encode()).decode()
components.html(f'<iframe src="data:text/html;base64,{b64_html}" style="
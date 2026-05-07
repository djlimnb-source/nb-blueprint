import streamlit as st
import streamlit.components.v1 as components
import base64

st.set_page_config(layout="wide", page_title="Blueprint Final")

st.title("🎮 블루프린트 에디터")
st.markdown("- **노드 배치**: 3개의 노드가 겹치지 않게 멀리 배치되었습니다.")
st.markdown("- **선 선택**: 연결선을 클릭하면 **주황색**으로 변합니다. 그 상태에서 **Delete** 키를 누르면 삭제됩니다.")

# HTML/JS 코드를 변수에 담음
raw_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; background-color: #1a1a1a; overflow: hidden; font-family: sans-serif; }
        #rete { height: 100vh; width: 100vw; }
        /* 선 스타일: 기본 두께를 키워 클릭이 잘 되게 함 */
        .connection .main-path { stroke: #666; stroke-width: 6px !important; transition: all 0.2s; cursor: pointer; fill: none; }
        /* 선택된 선 하이라이트 */
        .connection.selected .main-path { stroke: #ff9d00 !important; filter: drop-shadow(0 0 10px #ff9d00); stroke-width: 8px !important; }
        .node { background: #252525 !important; border: 1px solid #444 !important; border-radius: 8px !important; min-width: 180px !important; }
        .node.selected { border: 2px solid #ff9d00 !important; }
        .node .title { background: #333 !important; color: #eee !important; padding: 12px !important; font-size: 15px; }
        .socket { width: 22px !important; height: 22px !important; margin: 8px !important; background: #888 !important; }
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
            constructor() { super("Blueprint Node"); }
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

            // 노드 3개를 겹치지 않게 확실히 벌림 (X: 100, 550, 1000)
            const n1 = await component.createNode({ x: 100, y: 150 });
            const n2 = await component.createNode({ x: 550, y: 400 });
            const n3 = await component.createNode({ x: 1000, y: 150 });

            editor.addNode(n1); editor.addNode(n2); editor.addNode(n3);
            editor.connect(n1.outputs.get('out'), n2.inputs.get('in'));
            editor.connect(n2.outputs.get('out'), n3.inputs.get('in'));

            let selectedConn = null;

            // 선 클릭 시 하이라이트 부여
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

            // 빈 화면 클릭 시 선택 해제
            editor.on('click', () => {
                if (selectedConn) {
                    const v = editor.view.connections.get(selectedConn);
                    if(v) v.el.classList.remove('selected');
                    selectedConn = null;
                }
            });

            // 삭제 키보드 이벤트
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

# 에러 방지용 Base64 인코딩 처리
b64_html = base64.b64encode(raw_html.encode()).decode()
# f-string 대신 .format()을 사용하여 중괄호 에러를 원천 차단
src_url = "data:text/html;base64,{0}".format(b64_html)
components.html('<iframe src="{0}" style="width:100%; height:750px; border:none;"></iframe>'.format(src_url), height=750)
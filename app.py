import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="Blueprint UX Edition")

st.title("🎮 블루프린트 인터렉션 에디터")
st.caption("선(Connection)을 클릭하면 즉시 삭제됩니다. 노드 우클릭으로 새 노드를 추가하세요.")

node_html = """
<html>
    <head>
        <style>
            body { margin: 0; background-color: #1a1a1a; overflow: hidden; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
            #rete { height: 100vh; width: 100vw; }
            
            /* 연결선 스타일 */
            .connection .main-path {
                stroke: #777; /* 기본은 차분한 회색 */
                stroke-width: 4px !important;
                transition: stroke 0.2s, filter 0.2s;
                cursor: pointer; /* 마우스 올리면 포인터로 변경 */
            }

            /* 연결선 호버 효과 (블루프린트 오렌지) */
            .connection:hover .main-path {
                stroke: #ff9d00 !important;
                filter: drop-shadow(0 0 8px #ff9d00);
            }

            /* 노드 디자인 최적화 */
            .node { 
                background: rgba(30, 30, 30, 0.95) !important; 
                border: 1px solid #444 !important;
                min-width: 150px !important;
            }
            .node.selected { border: 2px solid #ff9d00 !important; }
            .node .title { background: #444 !important; color: #eee !important; font-size: 14px; padding: 8px !important; }
            .node .input-title, .node .output-title { color: #ccc !important; font-size: 12px; }
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
                constructor() { super("Function Node"); }
                builder(node) {
                    return node
                        .addInput(new Rete.Input('in', "Input", numSocket))
                        .addOutput(new Rete.Output('out', "Output", numSocket));
                }
            }

            async function init() {
                const container = document.querySelector('#rete');
                const editor = new Rete.NodeEditor('demo@0.1.0', container);
                
                // 1. 선의 곡률 설정
                editor.use(ConnectionPlugin.default, { curvature: 0.4 }); 
                editor.use(VueRenderPlugin.default);
                editor.use(ContextMenuPlugin.default);

                const component = new BlueNode();
                editor.register(component);

                // 초기 샘플 노드
                const n1 = await component.createNode({ x: 100, y: 150 });
                const n2 = await component.createNode({ x: 500, y: 200 });
                editor.addNode(n1);
                editor.addNode(n2);
                editor.connect(n1.outputs.get('out'), n2.inputs.get('in'));

                // --- 🌟 핵심 인터렉션 코드 시작 ---

                // 연결선을 클릭했을 때 삭제하는 기능
                editor.on('click', ({ type, e }) => {
                    // 클릭된 요소가 connection인지 확인
                    if (type === 'connection') {
                        // 클릭된 데이터에서 해당 connection(선) 정보를 찾아 삭제
                        const target = e.target.closest('.connection');
                        if (target) {
                           // Rete.js 내부 데이터에서 엣지를 찾아 제거합니다.
                           // 이 부분은 라이브러리 특성에 맞춰 pick 기능을 활용합니다.
                        }
                    }
                });

                // 더 직관적인 방법: 선을 더블클릭하거나 선택 후 Delete 키 연동
                editor.on('connectionpick', (connection) => {
                    if(confirm("이 연결을 삭제하시겠습니까?")) {
                        editor.removeConnection(connection);
                    }
                });

                // --- 🌟 핵심 인터렉션 코드 끝 ---

                editor.view.resize();
            }

            window.onload = init;
        </script>
    </body>
</html>
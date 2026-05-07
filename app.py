import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="Blueprint Standard UX")

st.title("🎮 블루프린트 표준 노드 에디터")
st.markdown("""
- **노드 3개 초기 배치**: 겹치지 않게 정렬되어 시작됩니다.
- **표준 조작**: 연결선을 클릭하면 주황색으로 강조되며, **Delete** 키로 삭제 가능합니다.
- **선 재연결**: 입력단(Input)의 선 끝을 드래그하여 다른 곳으로 옮길 수 있습니다.
""")

# HTML/JS/CSS 통합 코드
node_editor_code = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; background-color: #1a1a1a; overflow: hidden; font-family: sans-serif; }
        #rete { height: 100vh; width: 100vw; }
        
        /* 연결선(Connection) 스타일 */
        .connection .main-path {
            stroke: #666;
            stroke-width: 4px !important;
            transition: all 0.2s;
            cursor: pointer;
        }

        /* 선 선택 시 하이라이트 (블루프린트 오렌지) */
        .connection.selected .main-path {
            stroke: #ff9d00 !important;
            filter: drop-shadow(0 0 8px #ff9d00);
            stroke-width: 6px !important;
        }

        /* 노드 스타일 */
        .node { background: #252525 !important; border: 1px solid #444 !important; border-radius: 8px !important; }
        .node.selected { border: 2px solid #ff9d00 !important; }
        .node .title { background: #333 !important; color: #eee !important; padding: 10px !important; font-size: 14px; border-radius: 6px 6px 0 0; }
        
        /* 소켓(연결점) 스타일 */
        .socket { width: 16px !important; height: 16px !important; margin: 6px !important; }
    </style>
</head>
<body>
    <div id="rete"></div>

    <script src="https://cdn.jsdelivr.net/npm/vue@2.6.14/dist/vue.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/rete@1.4.5/build/rete.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/rete-vue-render-plugin@0.5.0/build/vue-render-plugin.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/rete-connection-plugin@0.9.0/build/
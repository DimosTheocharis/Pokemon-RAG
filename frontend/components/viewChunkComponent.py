import streamlit as st
from typing import TypedDict

class ChunkInformation(TypedDict):
    rank: int
    score: float
    fileΝame: str
    text: str
    metadata: dict


@st.dialog("Chunk Inspection", dismissible=True, on_dismiss="ignore", width="medium")
def viewChunkComponent(chunk: ChunkInformation):
    '''
        Renders a dialog component to view detailed information about a specific chunk.
        The dialog contains two tabs: "General Information" and "Metadata".
    '''
    tab1, tab2 = st.tabs(["General Information", "Metadata"])

    with tab1:
        st.header("General Information")

        badgesContainer = st.container(key="badgesContainer", horizontal=True, horizontal_alignment="left")

        if 'rank' in chunk:
            badgesContainer.badge(label=f"#{chunk['rank']}", color="orange", icon="🏆")

        if 'score' in chunk:
            badgesContainer.badge(label=f"{chunk['score']}", color="violet", icon="🎯")

        if 'fileName' in chunk:
            badgesContainer.badge(label=f"{chunk['fileName']}", color="green", icon="📁")

        st.text_area(label="Text", value=chunk["text"], disabled=True, height=250)

    with tab2:
        st.header("Metadata")

        if 'metadata' in chunk:
            st.dataframe(chunk["metadata"])
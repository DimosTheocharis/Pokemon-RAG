import streamlit as st
import uuid
from frontend.components.viewChunkComponent import viewChunkComponent, ChunkInformation

def retrievedChunksTableComponent(data: list[ChunkInformation]):
    textMaximumLength = 100
    with st.expander("Retrieved chunks:"):
        columnLengths = [1, 1, 2, 4, 2]
        # Header
        h1, h2, h3, h4, h5 = st.columns(columnLengths)

        h1.write("Rank")
        h2.write("Score")
        h3.write("Filename")
        h4.write("Text")
        h5.write("Inspect")

        # Rows
        for chunk in data:
            c1, c2, c3, c4, c5 = st.columns(columnLengths)

            c1.write(chunk["rank"])
            c2.write(chunk["score"])
            c3.write(chunk["fileName"])
            c4.write(chunk["text"][:textMaximumLength] + "...")

            c5.button("👁️", key=str(uuid.uuid1()), use_container_width=True, on_click=viewChunkComponent, args=[chunk])
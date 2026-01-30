import json
import streamlit as st

def load_data():
    with open("data/raw/book1.json", "r", encoding="utf-8") as f:
        return json.load(f)

def search(query, data):
    query = query.lower()
    score = 0

    # Caption
    if data.get("caption") and query in data["caption"]["text"].lower():
        score += 2

    # Tags
    for tag in data.get("tags", []):
        if query in tag["text"].lower():
            score += 1

    # Objects
    for obj in data.get("objects", []):
        if obj.get("name") and query in obj["name"].lower():
            score += 2

    # OCR
    for line in data.get("read", []):
        if query in line["line"].lower():
            score += 2
        for w in line["words"]:
            if query in w.lower():
                score += 1

    return score

# ================================
# DEMO UI — "검색만 보여줌"
# ================================

st.title("이미지 검색 데모")

query = st.text_input("검색어 입력")

if query:
    data = load_data()
    score = search(query, data)

    if score > 0:
        st.write(f"검색 결과 스코어: {score}")

        # 이미지 표시
        st.image(data["image_url"], caption=data["caption"]["text"])

        st.write("Tags:", ", ".join([t["text"] for t in data.get("tags", [])]))

        if data.get("objects"):
            st.write("Object:")
            for o in data["objects"]:
                st.write(f"- {o['name']} (conf={o['confidence']})")

        if data.get("read"):
            st.write("OCR 텍스트:")
            for line in data["read"]:
                st.write("- " + line["line"])
    else:
        st.write("검색 결과 없음.")

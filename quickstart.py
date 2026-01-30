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
    if "tags" in data:
        for tag in data["tags"]:
            if query in tag["text"].lower():
                score += 1

    # Objects
    if "objects" in data:
        for obj in data["objects"]:
            if obj["name"] and query in obj["name"].lower():
                score += 2  # 객체는 의미적 중요도가 높으므로 가중치 2

    # OCR
    if "read" in data:
        for line in data["read"]:
            if query in line["line"].lower():
                score += 2
            for w in line["words"]:
                if query in w.lower():
                    score += 1

    return score

# ================================
# Streamlit UI
# ================================
st.title("이미지 JSON 기반 검색 데모")

search_query = st.text_input("검색어 입력", "")

if search_query:
    data = load_data()
    score = search(search_query, data)

    if score > 0:
        st.write(f"검색 스코어: {score}")
        st.image(data["image_url"], caption=data["caption"]["text"])

        st.write("태그:", ", ".join([t["text"] for t in data["tags"]]))

        if "objects" in data:
            st.write("객체 목록:")
            for obj in data["objects"]:
                bbox = obj["bounding_box"]
                st.write(f"- {obj['name']} (confidence={obj['confidence']}, bbox={bbox})")

        if "read" in data:
            st.write("OCR 텍스트:")
            for line in data["read"]:
                st.write("- " + line["line"])
    else:
        st.write("검색 결과 없음.")

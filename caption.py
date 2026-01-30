import os
import json
#azure 이미지 분석을 위해 도구 가져오기
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential


def analyze_image(image_url: str, save_name: str):
    #자신의 azure 계정 연결설정
    endpoint = "***" #본인의 endpoint 입력력
    key = "***"  # 본인의 KEY 입력

    client = ImageAnalysisClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key)
    )

    # 모델이 이미지의 어떤 부분을 분석할지 결정.
    result = client.analyze_from_url(
        image_url=image_url,
        visual_features=[
            VisualFeatures.CAPTION,
            VisualFeatures.TAGS,
            VisualFeatures.OBJECTS
        ],
        gender_neutral_caption=True
    )

    #---Pixel을 데이터로 만들기 위한 준비 과정---

    print("=== Image Analysis Results ===")

    # CAPTION 추출
    caption_data = None
    if result.caption is not None:
        caption_data = {
            "text": result.caption.text,
            "confidence": result.caption.confidence
        }
        print(f"Caption: {caption_data['text']} ({caption_data['confidence']:.4f})")

    # TAG 추출
    tags_data = []
    if result.tags is not None and result.tags.list:
        print("\nTags:")
        for t in result.tags.list:
            print(f" - {t.name}")
            tags_data.append({
                "text": t.name,
                "confidence": t.confidence
            })

    # OBJECTS 추출
    objects_data = []
    if result.objects is not None and result.objects.list:
        print("\nObjects:")
        for obj in result.objects.list:

            # 객체 라벨 & confidence (tags[0] 사용)
            label = obj.tags[0].name if obj.tags else None
            confidence = obj.tags[0].confidence if obj.tags else None

            bbox = obj.bounding_box
            bbox_data = {
                "x": bbox.x,
                "y": bbox.y,
                "width": bbox.width,
                "height": bbox.height
            } if bbox else None

            print(f" - {label} ({confidence:.4f})" if confidence else f" - {label}")

            objects_data.append({
                "name": label,
                "confidence": confidence,
                "bounding_box": bbox_data
            })
    # 이미지 분석 끝

    # 모델이 찾아낸 정보를 JSON데이터로 출력
    # 다른분야에서 활용하기 위한 Index 구조 설정.(데이터 구조화)
    output = {
        "image_url": image_url,
        "caption": caption_data,
        "tags": tags_data,
        "objects": objects_data
    }
      
    # 이후 해당 결과를 JSON 파일형태로 저장
    os.makedirs("data/raw", exist_ok=True)
    save_path = os.path.join("data/raw", f"{save_name}.json")

    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\nJSON saved to: {save_path}")


if __name__ == "__main__":
    #이미지 url 저장
    test_image_url = "https://img.khan.co.kr/news/r/1100xX/2024/01/17/news-p.v1.20240117.bf7271484d6d4ef4857680cad82e997d.webp"
    #분석 시작
    analyze_image(test_image_url, "book1")

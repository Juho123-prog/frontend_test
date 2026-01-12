import requests


def introspect_token(access_token: str, client_secret: str = "") -> dict:
    """
    Keycloak의 토큰 인트로스펙션 엔드포인트를 호출하여 토큰의 활성화 여부(active)를 확인합니다.

    매개변수:
      - access_token: 검증할 액세스 토큰
      - client_secret: (필요시) 클라이언트 시크릿

    반환:
      - 토큰 상태 정보(JSON), 예를 들어 {"active": True, ...}
    """
    introspect_url = "https://auth.mobilex.kr/realms/mobilex/protocol/openid-connect/token/introspect"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    payload = {
        "client_id": "autox",
        "token": access_token
    }
    if client_secret:
        payload["client_secret"] = client_secret

    try:
        response = requests.post(introspect_url, headers=headers, data=payload)
        response.raise_for_status()
    except requests.RequestException as e:
        print("인트로스펙션 요청 실패:", e)
        return None

    result = response.json()
    if result.get("active"):
        print("토큰이 유효합니다.")
    else:
        print("토큰이 유효하지 않습니다.")
    return result


# 사용 예:
if __name__ == "__main__":
    # 위에서 받은 token_data에서 액세스 토큰을 추출합니다.
    token = "access_token"
    secret = "secret"
    introspect_result = introspect_token(token, secret)
    print("인트로스펙션 결과:", introspect_result)
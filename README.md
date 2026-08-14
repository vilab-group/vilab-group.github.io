# 연구실 홈페이지 (GitHub Pages / Jekyll)

`cg.postech.ac.kr`의 정보 구조를 그대로 가져오되, WordPress 대신 **Jekyll +
GitHub Pages**로 옮기고 색을 **파란색 계열**로 바꾼 스캐폴드입니다.

---

## 1. 바로 확인하기

`preview.html`을 브라우저로 열면 됩니다. Ruby 설치 없이 디자인 전체를 볼 수
있는 단일 파일 스냅샷입니다. (CSS가 인라인되어 있으니, 실제 수정은
`assets/css/main.css` 쪽에 하세요.)

## 2. 로컬에서 실행

```bash
gem install bundler
bundle install
bundle exec jekyll serve --livereload   # http://localhost:4000
```

## 3. 배포

1. 새 저장소를 만들고 이 폴더 내용을 push (`main` 브랜치)
2. Settings → Pages → Source를 **Deploy from a branch** → `main` / `(root)`
3. `_config.yml`의 `url`, `baseurl` 수정
   - `USERNAME.github.io` 저장소면 `baseurl: ""`
   - `USERNAME.github.io/lab` 형태면 `baseurl: "/lab"`
4. 학교 도메인(`xxx.univ.ac.kr`)을 쓰려면 루트에 `CNAME` 파일 하나 만들어
   도메인만 적고, 전산실에 CNAME 레코드를 `USERNAME.github.io`로 요청

`.github/workflows/pages.yml`은 선택 사항입니다. `github-pages` gem이 고정하는
Jekyll 버전보다 최신을 쓰거나 플러그인을 추가하고 싶을 때만 켜세요
(Settings → Pages → Source를 **GitHub Actions**로 변경).

---

## 4. 콘텐츠 수정 위치

HTML은 건드릴 일이 거의 없습니다. 아래 YAML만 고치면 됩니다.

| 파일 | 내용 |
|---|---|
| `_config.yml` | 연구실 이름, 주소, 이메일, 지도 embed, 소셜 링크 |
| `_data/nav.yml` | 상단 메뉴 |
| `_data/news.yml` | 소식 (최신순으로 위에 추가) |
| `_data/research.yml` | 연구 분야 |
| `_data/publications.yml` | 논문 목록 (`year`로 자동 그룹핑) |
| `_data/members.yml` | 구성원 (그룹별) |
| `_data/alumni.yml` | 졸업생 |

### 논문 한 편 추가 예시

```yaml
- year: 2026
  title: "논문 제목"
  authors: "<strong>학생 이름</strong>, 공저자, <strong>교수님 성함</strong>"
  venue: "MICCAI 2026"
  thumb: "/assets/img/pubs/miccai26.png"   # 없으면 "" 로 두면 그라디언트 처리
  links:
    - { label: "Paper", url: "https://arxiv.org/abs/..." }
    - { label: "Code",  url: "https://github.com/..." }
```

`<strong>`으로 감싼 이름이 굵게 표시됩니다 (연구실 멤버 표시 용도).

### 사진

`assets/img/people/`, `assets/img/pubs/`, `assets/img/news/`에 넣고 YAML에서
경로를 적으면 됩니다. 인물 사진은 3:4 비율, 600×800px 정도면 충분합니다.
경로를 비워두면 파란 그라디언트 플레이스홀더가 나옵니다.

---

## 5. 색 바꾸기

`assets/css/main.css` 맨 위 `:root` 블록의 값 6개가 전부입니다.

```css
--navy:    #0B1E33;  /* 어두운 배경 (히어로, 푸터) */
--navy-2:  #123252;  /* 어두운 면 위의 카드 */
--blue:    #12508C;  /* 메인 — 제목, 강조 */
--blue-lt: #2B7FC4;  /* 링크, 호버 */
--beam:    #3FBBD8;  /* 포인트 — 십자선, 스캔라인, 밑줄 */
--paper:   #F4F8FC;  /* 페이지 배경 */
```

레퍼런스 사이트의 자주색은 전부 이 스케일로 치환했습니다. 더 짙은 남색을
원하시면 `--navy`를 `#071726`, 더 밝고 활기찬 톤이면 `--blue`를 `#1565C0`
정도로 올리면 됩니다. 나머지는 따라옵니다.

---

## 6. 디자인 메모

- **히어로의 격자 + 스캔라인**: DICOM 뷰어의 좌표선과 위성 타일 그리드가
  같은 시각 언어라는 점에서 가져왔습니다. 이 사이트에서 유일하게 "튀는"
  요소이고, 나머지는 의도적으로 조용하게 뒀습니다.
- **타이포**: 제목 Space Grotesk / 본문 Pretendard(한글) / 라벨·연도·학회명은
  IBM Plex Mono. 학회명과 연도를 모노스페이스로 두면 논문 목록이 훨씬 잘
  스캔됩니다.
- **섹션 머리의 `+`**: 정합(registration) 마커에서 따온 것으로, 모든 섹션
  라벨 앞에 붙습니다.
- 모바일 대응, 키보드 포커스 표시, `prefers-reduced-motion`(스캔라인 정지)은
  모두 처리되어 있습니다.

## 7. 라이선스

콘텐츠와 코드 모두 자유롭게 수정해서 쓰세요.
# vilab_koreatech.github.io

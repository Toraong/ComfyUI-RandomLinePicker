# ComfyUI-RandomLinePicker

텍스트 파일(.txt)들이 있는 폴더에서 무작위로 여러 파일을 선택하고, 각 파일에서 지정한 개수만큼의 라인을 랜덤으로 추출하여 결합해주는 ComfyUI 커스텀 노드 모음입니다.

---

## 제공되는 노드 목록

1. **Random Text Line Picker (1 Folder)**
   - 1개 폴더를 대상으로 텍스트 라인을 무작위 추출합니다.
2. **Random Text Line Picker (3 Folders)**
   - 3개 폴더를 각각 설정하여 라인을 추출합니다.
   - 전체 결합된 `text` 외에도 각 폴더별 결과인 `text_1`, `text_2`, `text_3`을 각각 출력할 수 있습니다.
3. **Random Text Line Picker (5 Folders)**
   - 5개 폴더를 각각 설정하여 라인을 추출합니다.
   - 전체 결합된 `text` 외에도 각 폴더별 결과인 `text_1` ~ `text_5`를 각각 개별 출력할 수 있습니다.

---

## 주요 설정값

- **`folder_path_N`** (STRING): 텍스트 파일들이 있는 각 폴더 경로 (미사용 폴더는 비워두거나 `file_count`를 0으로 설정 가능)
- **`file_count_N`** (INT): 해당 폴더에서 선택할 텍스트 파일 개수 (0으로 설정 시 해당 폴더 건너뜀)
- **`lines_per_file_N`** (INT): 선택된 파일에서 추출할 라인 개수
- **`include_subfolders`** (BOOLEAN): 하위 폴더 포함 여부
- **`seed`** (INT): 랜덤 시드 값 (ComfyUI 컨트롤 메뉴에서 `randomize` 설정 시 매 생성마다 새로 추출)
- **`delimiter`** (선택, STRING): 추출된 라인들을 하나로 묶을 구분자 (기본값: `, `, `\n` 입력 시 개행 처리)
- **`strip_whitespace`** (선택, BOOLEAN): 앞뒤 공백 및 빈 줄 자동 제거 여부 (기본값: `True`)

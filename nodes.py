import os
import random
from pathlib import Path


def _read_file_lines(file_path: Path, strip: bool = True):
    """한글 및 다양한 인코딩 대응 (UTF-8, UTF-8-sig, CP949, EUC-KR 등)"""
    encodings = ["utf-8-sig", "utf-8", "cp949", "euc-kr", "latin-1"]
    for enc in encodings:
        try:
            with open(file_path, "r", encoding=enc) as f:
                raw_lines = f.readlines()

            if strip:
                lines = [line.strip() for line in raw_lines if line.strip()]
            else:
                lines = [line.rstrip("\r\n") for line in raw_lines if line.rstrip("\r\n")]
            return lines
        except (UnicodeDecodeError, Exception):
            continue
    return []


def _pick_from_folder(
    folder_path: str,
    include_subfolders: bool,
    file_count: int,
    lines_per_file: int,
    rng: random.Random,
    strip_whitespace: bool = True,
    tag: str = ""
):
    """지정된 폴더에서 파일과 라인을 무작위 추출"""
    clean_path = folder_path.strip().strip('"').strip("'")
    if not clean_path or file_count <= 0:
        return [], []

    target_dir = Path(clean_path)
    if not target_dir.exists() or not target_dir.is_dir():
        if clean_path:
            prefix = f"[{tag}] " if tag else ""
            print(f"{prefix}유효하지 않은 폴더 경로입니다: {clean_path}")
        return [], []

    pattern = "**/*.txt" if include_subfolders else "*.txt"
    txt_files = [p for p in target_dir.glob(pattern) if p.is_file()]

    if not txt_files:
        prefix = f"[{tag}] " if tag else ""
        print(f"{prefix}폴더 내에 .txt 파일이 없습니다: {clean_path}")
        return [], []

    # 정렬하여 시드 결정론적 보장
    txt_files.sort(key=lambda p: str(p))

    actual_file_count = min(file_count, len(txt_files))
    selected_files = rng.sample(txt_files, actual_file_count)

    picked_lines = []
    selected_file_names = []

    for file_path in selected_files:
        selected_file_names.append(file_path.name)
        lines = _read_file_lines(file_path, strip=strip_whitespace)
        if not lines:
            continue

        actual_lines_count = min(lines_per_file, len(lines))
        picked = rng.sample(lines, actual_lines_count)
        picked_lines.extend(picked)

    return picked_lines, selected_file_names


class RandomTextLinePicker:
    """1개 폴더에서 텍스트 라인을 무작위 추출하는 노드"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "folder_path": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "placeholder": "텍스트 파일들이 위치한 폴더 경로 (예: C:/prompts)"
                }),
                "include_subfolders": ("BOOLEAN", {
                    "default": True,
                    "label_on": "True (포함)",
                    "label_off": "False (미포함)"
                }),
                "file_count": ("INT", {
                    "default": 1,
                    "min": 1,
                    "max": 1000,
                    "step": 1,
                    "display": "number"
                }),
                "lines_per_file": ("INT", {
                    "default": 1,
                    "min": 1,
                    "max": 1000,
                    "step": 1,
                    "display": "number"
                }),
                "seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 0xffffffffffffffff,
                    "display": "number"
                }),
            },
            "optional": {
                "delimiter": ("STRING", {
                    "default": ", ",
                    "multiline": False,
                    "placeholder": "결과 결합 구분자 (예: ', ' 또는 \\n)"
                }),
                "strip_whitespace": ("BOOLEAN", {
                    "default": True,
                    "label_on": "True (공백/빈줄 제거)",
                    "label_off": "False (유지)"
                }),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("text", "selected_files")
    FUNCTION = "pick_lines"
    CATEGORY = "utils/text"

    @classmethod
    def IS_CHANGED(cls, folder_path, include_subfolders, file_count, lines_per_file, seed, **kwargs):
        return seed

    def pick_lines(
        self,
        folder_path: str,
        include_subfolders: bool,
        file_count: int,
        lines_per_file: int,
        seed: int,
        delimiter: str = ", ",
        strip_whitespace: bool = True
    ):
        rng = random.Random(seed)
        lines, files = _pick_from_folder(
            folder_path=folder_path,
            include_subfolders=include_subfolders,
            file_count=file_count,
            lines_per_file=lines_per_file,
            rng=rng,
            strip_whitespace=strip_whitespace,
            tag="RandomTextLinePicker"
        )

        formatted_delimiter = delimiter.replace("\\n", "\n").replace("\\t", "\t")
        combined_text = formatted_delimiter.join(lines)
        file_list_text = "\n".join(files)

        return (combined_text, file_list_text)


class RandomTextLinePicker3Folders:
    """3개 폴더에서 텍스트 라인을 무작위 추출하는 노드"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "folder_path_1": ("STRING", {"default": "", "multiline": False, "placeholder": "폴더 1 경로"}),
                "file_count_1": ("INT", {"default": 1, "min": 0, "max": 1000, "step": 1}),
                "lines_per_file_1": ("INT", {"default": 1, "min": 1, "max": 1000, "step": 1}),

                "folder_path_2": ("STRING", {"default": "", "multiline": False, "placeholder": "폴더 2 경로 (선택)"}),
                "file_count_2": ("INT", {"default": 1, "min": 0, "max": 1000, "step": 1}),
                "lines_per_file_2": ("INT", {"default": 1, "min": 1, "max": 1000, "step": 1}),

                "folder_path_3": ("STRING", {"default": "", "multiline": False, "placeholder": "폴더 3 경로 (선택)"}),
                "file_count_3": ("INT", {"default": 1, "min": 0, "max": 1000, "step": 1}),
                "lines_per_file_3": ("INT", {"default": 1, "min": 1, "max": 1000, "step": 1}),

                "include_subfolders": ("BOOLEAN", {
                    "default": True,
                    "label_on": "True (포함)",
                    "label_off": "False (미포함)"
                }),
                "seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 0xffffffffffffffff,
                    "display": "number"
                }),
            },
            "optional": {
                "delimiter": ("STRING", {
                    "default": ", ",
                    "multiline": False,
                    "placeholder": "결과 결합 구분자 (예: ', ' 또는 \\n)"
                }),
                "strip_whitespace": ("BOOLEAN", {
                    "default": True,
                    "label_on": "True (공백/빈줄 제거)",
                    "label_off": "False (유지)"
                }),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("text", "text_1", "text_2", "text_3", "selected_files")
    FUNCTION = "pick_lines"
    CATEGORY = "utils/text"

    @classmethod
    def IS_CHANGED(cls, seed, **kwargs):
        return seed

    def pick_lines(
        self,
        folder_path_1: str,
        file_count_1: int,
        lines_per_file_1: int,
        folder_path_2: str,
        file_count_2: int,
        lines_per_file_2: int,
        folder_path_3: str,
        file_count_3: int,
        lines_per_file_3: int,
        include_subfolders: bool,
        seed: int,
        delimiter: str = ", ",
        strip_whitespace: bool = True
    ):
        rng = random.Random(seed)
        formatted_delimiter = delimiter.replace("\\n", "\n").replace("\\t", "\t")

        configs = [
            (folder_path_1, file_count_1, lines_per_file_1, "Folder 1"),
            (folder_path_2, file_count_2, lines_per_file_2, "Folder 2"),
            (folder_path_3, file_count_3, lines_per_file_3, "Folder 3"),
        ]

        all_lines = []
        all_files = []
        folder_texts = []

        for path, f_cnt, l_cnt, tag in configs:
            lines, files = _pick_from_folder(
                folder_path=path,
                include_subfolders=include_subfolders,
                file_count=f_cnt,
                lines_per_file=l_cnt,
                rng=rng,
                strip_whitespace=strip_whitespace,
                tag=f"RandomTextLinePicker3Folders - {tag}"
            )
            folder_texts.append(formatted_delimiter.join(lines))
            all_lines.extend(lines)
            all_files.extend(files)

        combined_text = formatted_delimiter.join(all_lines)
        file_list_text = "\n".join(all_files)

        return (combined_text, folder_texts[0], folder_texts[1], folder_texts[2], file_list_text)


class RandomTextLinePicker5Folders:
    """5개 폴더에서 텍스트 라인을 무작위 추출하는 노드"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "folder_path_1": ("STRING", {"default": "", "multiline": False, "placeholder": "폴더 1 경로"}),
                "file_count_1": ("INT", {"default": 1, "min": 0, "max": 1000, "step": 1}),
                "lines_per_file_1": ("INT", {"default": 1, "min": 1, "max": 1000, "step": 1}),

                "folder_path_2": ("STRING", {"default": "", "multiline": False, "placeholder": "폴더 2 경로 (선택)"}),
                "file_count_2": ("INT", {"default": 1, "min": 0, "max": 1000, "step": 1}),
                "lines_per_file_2": ("INT", {"default": 1, "min": 1, "max": 1000, "step": 1}),

                "folder_path_3": ("STRING", {"default": "", "multiline": False, "placeholder": "폴더 3 경로 (선택)"}),
                "file_count_3": ("INT", {"default": 1, "min": 0, "max": 1000, "step": 1}),
                "lines_per_file_3": ("INT", {"default": 1, "min": 1, "max": 1000, "step": 1}),

                "folder_path_4": ("STRING", {"default": "", "multiline": False, "placeholder": "폴더 4 경로 (선택)"}),
                "file_count_4": ("INT", {"default": 1, "min": 0, "max": 1000, "step": 1}),
                "lines_per_file_4": ("INT", {"default": 1, "min": 1, "max": 1000, "step": 1}),

                "folder_path_5": ("STRING", {"default": "", "multiline": False, "placeholder": "폴더 5 경로 (선택)"}),
                "file_count_5": ("INT", {"default": 1, "min": 0, "max": 1000, "step": 1}),
                "lines_per_file_5": ("INT", {"default": 1, "min": 1, "max": 1000, "step": 1}),

                "include_subfolders": ("BOOLEAN", {
                    "default": True,
                    "label_on": "True (포함)",
                    "label_off": "False (미포함)"
                }),
                "seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 0xffffffffffffffff,
                    "display": "number"
                }),
            },
            "optional": {
                "delimiter": ("STRING", {
                    "default": ", ",
                    "multiline": False,
                    "placeholder": "결과 결합 구분자 (예: ', ' 또는 \\n)"
                }),
                "strip_whitespace": ("BOOLEAN", {
                    "default": True,
                    "label_on": "True (공백/빈줄 제거)",
                    "label_off": "False (유지)"
                }),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("text", "text_1", "text_2", "text_3", "text_4", "text_5", "selected_files")
    FUNCTION = "pick_lines"
    CATEGORY = "utils/text"

    @classmethod
    def IS_CHANGED(cls, seed, **kwargs):
        return seed

    def pick_lines(
        self,
        folder_path_1: str,
        file_count_1: int,
        lines_per_file_1: int,
        folder_path_2: str,
        file_count_2: int,
        lines_per_file_2: int,
        folder_path_3: str,
        file_count_3: int,
        lines_per_file_3: int,
        folder_path_4: str,
        file_count_4: int,
        lines_per_file_4: int,
        folder_path_5: str,
        file_count_5: int,
        lines_per_file_5: int,
        include_subfolders: bool,
        seed: int,
        delimiter: str = ", ",
        strip_whitespace: bool = True
    ):
        rng = random.Random(seed)
        formatted_delimiter = delimiter.replace("\\n", "\n").replace("\\t", "\t")

        configs = [
            (folder_path_1, file_count_1, lines_per_file_1, "Folder 1"),
            (folder_path_2, file_count_2, lines_per_file_2, "Folder 2"),
            (folder_path_3, file_count_3, lines_per_file_3, "Folder 3"),
            (folder_path_4, file_count_4, lines_per_file_4, "Folder 4"),
            (folder_path_5, file_count_5, lines_per_file_5, "Folder 5"),
        ]

        all_lines = []
        all_files = []
        folder_texts = []

        for path, f_cnt, l_cnt, tag in configs:
            lines, files = _pick_from_folder(
                folder_path=path,
                include_subfolders=include_subfolders,
                file_count=f_cnt,
                lines_per_file=l_cnt,
                rng=rng,
                strip_whitespace=strip_whitespace,
                tag=f"RandomTextLinePicker5Folders - {tag}"
            )
            folder_texts.append(formatted_delimiter.join(lines))
            all_lines.extend(lines)
            all_files.extend(files)

        combined_text = formatted_delimiter.join(all_lines)
        file_list_text = "\n".join(all_files)

        return (
            combined_text,
            folder_texts[0],
            folder_texts[1],
            folder_texts[2],
            folder_texts[3],
            folder_texts[4],
            file_list_text,
        )

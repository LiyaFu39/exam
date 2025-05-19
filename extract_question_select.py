import argparse
import json
import pathlib
import re

from PyPDF2 import PdfReader



def extract_mc_questions(text):
    pattern = r'(\d+)(\d)(.*?？)(.*?。)(.*?。)(.*?。)(.*?。)'
    matches = re.findall(pattern, text, re.DOTALL)

    questions = []
    for index, answer, question, *options in matches:
        questions.append({
            "題號": index,
            "答案": answer,
            "題目": question,
            "選項": options,
            "法源": "",
        })

    return questions


def main(args):
    inp = pathlib.Path(args.inp)
    
    reader = PdfReader(str(inp))
    chapters = {}

    context = ""
    curr_chapter = ""
    for page in reader.pages:
        # 0. 抽取文字和移除換行符號
        text = page.extract_text()
        # 1. 移除「資料產生日期」和頁碼、編號、答案、試題字樣
        text = re.sub(r"資料產生日期：\d{3}/\d{2}/\d{2}", "", text)
        text = text.replace("編號答案試題", "")
        match = re.search(r'\n[\u4e00-\u9fff]+?\n選擇題', text)
        if match:
            chapter = match.group(0).replace("\n", "").replace("選擇題", "")
            prev_index, next_index = match.span()
            if curr_chapter:
                chapters[curr_chapter] += text[:prev_index]
            curr_chapter = chapter
            chapters[curr_chapter] = text[next_index:]
            continue
        chapters[curr_chapter] += text

    for key in chapters:
        context = chapters[key]
        context = context.replace("\n", "").replace(" ", "")
        chapters[key] = extract_mc_questions(context)
        
        # # 2. 捕獲章節名稱（透過「選擇題」前的文字判斷）
        # section_pattern = r"([^\d\n]+?)\s*(選擇題|是非題)"
        # section_match = re.search(section_pattern, text)
        # if section_match:
        #     current_section = section_match.group(1).strip()
        #     if current_section not in chapters:
        #         chapters[current_section] = []
    
        # 3. 捕獲題號、答案、題目
        # pattern = r"(\d+)\s+([OX]|\d+)(.*?)(?=\d+\s+[OX]|\d+\s+\d+|$)"  # 題號、答案、內容
        # matches = re.findall(pattern, text, re.DOTALL)
        # for number, answer, content in matches:
        #     content = content.strip()
        #     # content = content.replace(" ", "")
    
        #     # 法源例外處理
        #     note_match = re.search(r"(第\s*\d+\s*條)$", content)
        #     note = note_match.group(1).strip() if note_match else ""
        #     if note:
        #         content = content[:note_match.start()].strip()
    
        #     # 拆分題目與選項（保留 (1)(2)... 並切分）
        #     option_matches = list(re.finditer(r'\(\d\)', content))
        #     if option_matches:
        #         question_text = content[:option_matches[0].start()].strip()
        #         options = []
        #         for i in range(len(option_matches)):
        #             start = option_matches[i].start()
        #             end = option_matches[i + 1].start() if i + 1 < len(option_matches) else len(content)
        #             option = content[start:end].strip()
        #             options.append(option)
        #     else:
        #         question_text = content
        #         options = []
    
        #     question = {
        #         "題號": number,
        #         "答案": answer,
        #         "題目": question_text,
        #         "選項": options if options else ["O", "X"],
        #         "法源": note
        #     }
            
        #     if current_section:
        #         chapters[current_section].append(question)
    
    # 匯出為 JSON 檔案
    with open(inp.stem + ".json", "w", encoding="utf-8") as f:
        json.dump(chapters, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("inp", type=str, help="input pdf file")
    args = parser.parse_args()
    main(args)

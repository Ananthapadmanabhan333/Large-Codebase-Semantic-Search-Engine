from tree_sitter_language_pack import get_language, get_parser
from typing import List, Dict, Any
import os

class CodeParser:
    def __init__(self):
        # Supported languages
        self.languages = {
            ".py": "python",
            ".js": "javascript",
            ".ts": "typescript",
            ".tsx": "tsx",
            ".go": "go",
            ".rs": "rust",
            ".java": "java",
            ".cpp": "cpp",
            ".c": "c"
        }
        self.parsers = {}

    def get_parser_for_ext(self, ext: str):
        lang_name = self.languages.get(ext)
        if not lang_name:
            return None
        
        if lang_name not in self.parsers:
            self.parsers[lang_name] = get_parser(lang_name)
        
        return self.parsers[lang_name]

    def parse_file(self, file_path: str) -> Dict[str, Any]:
        ext = os.path.splitext(file_path)[1]
        parser = self.get_parser_for_ext(ext)
        if not parser:
            return {"symbols": [], "content": ""}

        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        tree = parser.parse(content)
        root_node = tree.root_node()

        symbols = self._extract_symbols(root_node, content, ext)
        
        return {
            "symbols": symbols,
            "content": content
        }

    def _extract_symbols(self, node, content, ext) -> List[Dict]:
        symbols = []
        
        target_kinds = {
            "function_definition", "class_definition", "method_definition",
            "arrow_function", "function_declaration", "interface_declaration",
            "type_alias_declaration", "enum_declaration"
        }

        def traverse(n):
            kind = n.kind()
            if kind in target_kinds:
                name = self._get_node_name(n, content)
                symbols.append({
                    "name": name,
                    "type": kind,
                    "start_line": n.start_position().row,
                    "end_line": n.end_position().row,
                    "content": content[n.start_byte():n.end_byte()]
                })
            
            for i in range(n.child_count()):
                child = n.child(i)
                traverse(child)

        traverse(node)
        return symbols

    def _get_node_name(self, node, content) -> str:
        for i in range(node.child_count()):
            child = node.child(i)
            if child.kind() == "identifier":
                return content[child.start_byte():child.end_byte()]
        return "anonymous"

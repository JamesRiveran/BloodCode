import React from "react";
import CodeMirror from "@uiw/react-codemirror";
import { oneDark } from "@codemirror/theme-one-dark";
import { autocompletion, completeFromList } from "@codemirror/autocomplete";
import { StreamLanguage } from "@codemirror/language";

const cycles = ["Nightmare", "Dream"];
const declarations = ["Hunter", "Hunters", "GreatOnes", "Rom"];
const types = ["Djura", "Eileen", "Blood", "Maria", "Gehrman"];
const conditions = ["Insight", "Madness"];
const breaks = ["Rest"];
const vectors = ["Drunkenness"];
const data = ["Eyes", "Pray"];
const logicalOperators = ["Vileblood", "Bloodbond", "OldBlood"];

const bloodCodeLiterals = ["true", "false"];
const bloodCodeOperatorsAndSymbols = [
  ">", "<", ">=", "<=", "==", "=>", "!=", ":", "(", ")", "{", "}", ",",
  "[", "]", ";", "+", "-", "*"
];

const bloodCodeKeywords = [
  ...cycles,
  ...declarations,
  ...types,
  ...conditions,
  ...breaks,
  ...vectors,
  ...data,
  ...logicalOperators
];

const bloodCodeTokens = [
  ...bloodCodeKeywords.map(k => ({ label: k, type: "keyword" })),
  ...bloodCodeLiterals.map(l => ({ label: l, type: "literal" })),
  ...bloodCodeOperatorsAndSymbols.map(op => ({ label: op, type: "operator" })),
];

const bloodCodeLanguage = StreamLanguage.define({
  token(stream) {
    if (stream.eatSpace()) return null;
    if (stream.match(/\/\/.*/)) return "comment";
    if (stream.match(/"(?:[^\\]|\\.)*?"/)) return "string";
    if (stream.match(/\d+/)) return "number";
    if (stream.match(new RegExp(`\\b(${cycles.join("|")})\\b`))) return "cycle";
    if (stream.match(new RegExp(`\\b(${declarations.join("|")})\\b`))) return "declaration";
    if (stream.match(new RegExp(`\\b(${types.join("|")})\\b`))) return "type";
    if (stream.match(new RegExp(`\\b(${conditions.join("|")})\\b`))) return "condition";
    if (stream.match(new RegExp(`\\b(${breaks.join("|")})\\b`))) return "break";
    if (stream.match(new RegExp(`\\b(${vectors.join("|")})\\b`))) return "vector";
    if (stream.match(new RegExp(`\\b(${data.join("|")})\\b`))) return "data";
    if (stream.match(new RegExp(`\\b(${logicalOperators.join("|")})\\b`))) return "logicalOperator";
    if (stream.match(new RegExp(`\\b(${bloodCodeLiterals.join("|")})\\b`))) return "literal";
    if (stream.match(/[+\-*\/=<>!]+/)) return "operator";
    if (stream.match(/[{}[\]()]/)) return "bracket";
    if (stream.match(/[a-zA-Z_][a-zA-Z0-9_]*/)) return "variable";
    stream.next();
    return null;
  },
});

export const CodeEditor: React.FC<{ code: string; setCode: (code: string) => void }> = ({ code, setCode }) => {
  return (
    <div className="flex-grow p-4 bg-gray-800 rounded-lg shadow-md w-full">
      <CodeMirror
        value={code}
        height="500px"
        theme={oneDark}
        extensions={[
          bloodCodeLanguage,
          autocompletion({ override: [completeFromList(bloodCodeTokens)] }),
        ]}
        onChange={(value) => setCode(value)}
      />
    </div>
  );
};

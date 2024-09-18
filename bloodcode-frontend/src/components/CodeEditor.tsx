"use client";
import React, { useRef } from "react";

interface CodeEditorProps {
  code: string;
  setCode: (code: string) => void;
  lineNumbers: string[];
}

export const CodeEditor: React.FC<CodeEditorProps> = ({ code, setCode, lineNumbers }) => {
  const editorRef = useRef<HTMLTextAreaElement>(null);

  const handleEditorScroll = (e: React.UIEvent<HTMLTextAreaElement>) => {
    const lineNumbersElement = editorRef.current?.previousElementSibling as HTMLElement;
    if (lineNumbersElement) {
      lineNumbersElement.scrollTop = e.currentTarget.scrollTop;
    }
  };

  return (
    <div className="flex-grow bg-gray-800 rounded-lg shadow-md flex overflow-hidden">
      <div className="p-4 text-right bg-gray-700 text-gray-500 select-none overflow-hidden h-[500px] max-h-[500px]">
        {lineNumbers.map((num) => (
          <div key={num} className="leading-6 h-6">{num}</div>
        ))}
      </div>
      <textarea
        ref={editorRef}
        value={code}
        onChange={(e) => setCode(e.target.value)}
        onScroll={handleEditorScroll}
        placeholder="Escribe tu código aquí"
        className="flex-grow h-[500px] max-h-[500px] p-4 bg-gray-800 text-gray-100 border-none resize-none focus:outline-none font-mono overflow-y-auto h-full"
      />
    </div>
  );
};

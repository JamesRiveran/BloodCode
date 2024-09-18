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

  const handleCodeChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setCode(e.target.value); 
  };

  return (
    <main className="flex-grow flex flex-col p-4 space-y-4 w-full h-full">
      <div className="flex-grow bg-color-gray-800 rounded-lg shadow-md flex overflow-hidden w-full h-full">
        
        <div className="p-4 text-right bg-color-gray-700 text-gray-400 select-none overflow-hidden flex-shrink-0 border border-gray-600">
          {lineNumbers.map((num) => (
            <div key={num} className="leading-6">{num}</div>
          ))}
        </div>
        
        <textarea
          ref={editorRef}
          value={code}  
          onChange={handleCodeChange} 
          onScroll={handleEditorScroll}  
          placeholder="Escribe tu código aquí"
          className="flex-grow p-4 bg-color-gray-800 text-gray-100 resize-none border border-gray-600 focus:outline-none font-mono overflow-y-auto w-full h-full"
        />
      </div>
    </main>
  );
};

import { Button } from "@/components/ui/button";
import { Trash2 } from "lucide-react"

interface OutputDisplayProps {
  output: string[];
  isError: boolean;
  isPromptActive: boolean;  
  handleUserInputKeyDown: (e: React.KeyboardEvent<HTMLDivElement>) => void;
  userInput: string; 
  clearOutput: () => void;
}

export const OutputDisplay: React.FC<OutputDisplayProps> = ({
  output,
  isError,
  isPromptActive,
  handleUserInputKeyDown,
  userInput,
  clearOutput
}) => {
  return (
    <div
      className="flex flex-col bg-color-gray-800 rounded-lg shadow-md p-6 w-full h-auto max-h-[70vh] space-y-4"
      tabIndex={0}
      onKeyDown={handleUserInputKeyDown}
    >
      <div className="flex-grow bg-color-gray-700 rounded-lg shadow-md p-4 overflow-hidden h-[29vh] flex flex-col">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-semibold text-gray-400">Consola</h2>
          <Button onClick={clearOutput} variant={"danger"}>
            <Trash2 />
          </Button>
        </div>

        <div className="flex-grow w-full overflow-y-auto bg-color-gray-800 p-5 rounded border border-gray-600 text-white">
          {output.map((line, index) => (
            <div key={index}>{line}</div>
          ))}
          {isPromptActive && (
            <div className="input-line">
              <span>{userInput}</span>
              <span className="blinking-cursor">_</span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

import { useState } from "react";
import axios from "axios";

const QnA = () => {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");

  const handleAsk = async () => {
    try {
      setAnswer("Thinking... 🤔");
      const response = await axios.post("http://localhost:8000/ask", {
        question
      });
      setAnswer(response.data.answer || "No answer returned!");
    } catch (error) {
      console.error(error);
      setAnswer("Error fetching answer ❌");
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-lg mt-6">
      <h2 className="text-xl font-semibold mb-2">❓ Ask a Question</h2>
      <input
        type="text"
        className="w-full p-2 border border-gray-300 rounded-lg mb-4"
        placeholder="Ask your question here"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />
      <button
        onClick={handleAsk}
        className="bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded"
      >
        Get Answer
      </button>

      {answer && (
        <div className="mt-4 text-blue-600 font-medium">
          🗣️ {answer}
        </div>
      )}
    </div>
  );
};

export default QnA;

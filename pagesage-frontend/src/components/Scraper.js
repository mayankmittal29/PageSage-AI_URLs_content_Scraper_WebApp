import { useState } from "react";
import axios from "axios";

const Scraper = () => {
  const [urls, setUrls] = useState("");
  const [message, setMessage] = useState("");

  const handleScrape = async () => {
    try {
      setMessage("Scraping in progress... 🕵️‍♂️");
      console.log(urls)
      const response = await axios.post("http://localhost:8000/scrape", {
        urls: urls.split(",").map(url => url.trim())
      });
      setMessage(response.data.message || "Scraping complete! 🎉");
    } catch (error) {
      console.error(error);
      setMessage("Error scraping URLs ❌");
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-lg mt-6">
      <h2 className="text-xl font-semibold mb-2">🔗 Enter URLs to Scrape</h2>
      <textarea
        rows="3"
        className="w-full p-2 border border-gray-300 rounded-lg mb-4"
        placeholder="Enter URLs separated by commas"
        value={urls}
        onChange={(e) => setUrls(e.target.value)}
      />
      <button
        onClick={handleScrape}
        className="bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded"
      >
        Scrape URLs
      </button>

      {message && (
        <div className="mt-4 text-green-600 font-medium">{message}</div>
      )}
    </div>
  );
};

export default Scraper;

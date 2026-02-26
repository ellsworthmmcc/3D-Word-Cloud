import axios from "axios";
import { API_BASE_URL, type ArticleResponse } from "../utils";
import { useState } from "react";



function SubmitURL() {
  const [url, setUrl] = useState("");
  const [data, setData] = useState<ArticleResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (el: React.FormEvent) => {
    el.preventDefault();
    setError(null);
    setData(null);

    if (!url.trim()) {
      setError("Please enter a URL");
      return;
    }

    try {
      setLoading(true);

      const response = await axios.post<ArticleResponse>(
        `${API_BASE_URL}`, { url }
      );

      setData(response.data);
    } catch (err: any) {
      if (err.response?.data?.detail) {
        setError(err.response.data.detail);
      } else {
        setError("An error has occured");
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      <form
        onSubmit={handleSubmit}
        className="w-full max-w-xl flex gap-3"
      >
        <input
          type="url"
          placeholder="Enter article URL..."
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          className="flex-1 px-4 py-2 rounded-lg bg-slate-800 border border-slate-700 focus:outline-none focus:ring-2 focus:ring-indigo-500"
        />

        <button
          type="submit"
          disabled={ loading }
          className="px-6 py-2 bg-indigo-600 rounded-lg hover:bg-indigo-500 disabled:opacity-50"
        >
          {loading ? "Processing..." : "Analyze"}
        </button>
      </form>

      {data && (
        <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
            {Object.entries(data.article_analysis).map(
              ([word, count]) => (
                <div
                  key={word}
                  className="bg-slate-800 p-3 rounded-lg flex justify-between"
                >
                  <span>{word}</span>
                  <span className="text-indigo-400">
                    {count}
                  </span>
                </div>
              )
            )}
        </div>
      )}
    </>
  )
}

export default SubmitURL
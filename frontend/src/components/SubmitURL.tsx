import axios from "axios";
import { API_BASE_URL, type ArticleResponse } from "../utils";
import { useState } from "react";
import CloudHolder from "./Cloud";

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
    } catch (err: unknown) {
      if (axios.isAxiosError(err)) {
        if (err.response?.data?.detail) {
          // Server responded with a specific error message
          setError(err.response.data.detail);
        } else if (err.request) {
          // Request was made but no response received (e.g. backend is down)
          setError("Could not reach the server. Is the backend running?");
        } else {
          // Something went wrong setting up the request
          setError("Failed to send request.");
        }
      } else {
        // Non-axios error (e.g. unexpected runtime error)
        setError("An unexpected error has occurred.");
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

      <div className="flex flex-col w-full gap-10">
        {(data && !loading) && (
          <div className="flex w-full h-full">
            <CloudHolder analysis={data?.article_analysis}/>
          </div>
        )}
        {error && (
          <div className="w-full flex items-center justify-center">
            <div className="text-red-500 text-xl font-semibold">
              That article cannot be analyzed. Try another one.
            </div>
          </div>
        )}

      </div>
    </>
  )
}

export default SubmitURL
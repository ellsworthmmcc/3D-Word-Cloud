export const API_BASE_URL = "/api/analyze"

export type ArticleResponse = {
  id: number,
  url: string,
  article_analysis: Record<string, number>,
  date_created: string,
  date_updated: string,
}
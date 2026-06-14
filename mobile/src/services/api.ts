import AsyncStorage from '@react-native-async-storage/async-storage';

const API_BASE = 'https://api.gold-analysis.example.com/v1';

class ApiService {
  private apiKey: string | null = null;

  async init() {
    this.apiKey = await AsyncStorage.getItem('api_key');
  }

  async setApiKey(key: string) {
    this.apiKey = key;
    await AsyncStorage.setItem('api_key', key);
  }

  private async request(endpoint: string, options: RequestInit = {}) {
    const headers = {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${this.apiKey}`,
      ...options.headers,
    };

    const response = await fetch(`${API_BASE}${endpoint}`, {
      ...options,
      headers,
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.status}`);
    }

    return response.json();
  }

  async getPrice() {
    return this.request('/market/price');
  }

  async getHistory(startDate: string, endDate: string) {
    return this.request(`/market/history?start_date=${startDate}&end_date=${endDate}`);
  }

  async getTechnicalAnalysis() {
    return this.request('/analysis/technical');
  }

  async getDecision() {
    return this.request('/decision/recommend');
  }

  async listPortfolios() {
    return this.request('/portfolio');
  }

  async createPortfolio(name: string, initialCapital: number) {
    return this.request('/portfolio', {
      method: 'POST',
      body: JSON.stringify({ name, initial_capital: initialCapital }),
    });
  }

  async createAlert(type: string, targetPrice: number, channels: string[]) {
    return this.request('/alert', {
      method: 'POST',
      body: JSON.stringify({ type, target_price: targetPrice, channels }),
    });
  }

  async listPosts(contentType?: string) {
    const params = contentType ? `?content_type=${contentType}` : '';
    return this.request(`/community/posts${params}`);
  }
}

export const api = new ApiService();

import WebSocket from 'ws';

export class JarvisClient {
  private socket?: WebSocket;
  private pending = new Map<string, (data: any) => void>();

  constructor(private url: string) {}

  async connect(): Promise<void> {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      return;
    }
    this.socket = new WebSocket(this.url);
    this.socket.on('message', (data: WebSocket.RawData) => {
      try {
        const msg = JSON.parse(data.toString());
        const id = msg.id;
        if (id && this.pending.has(id)) {
          const resolve = this.pending.get(id)!;
          this.pending.delete(id);
          resolve(msg);
        }
      } catch {
        // ignore parse errors
      }
    });
    await new Promise<void>((resolve, reject) => {
      this.socket?.once('open', () => resolve());
      this.socket?.once('error', (err: any) => reject(err));
    });
  }

  sendRequest(payload: any): Promise<any> {
    const id = Date.now().toString() + Math.random().toString();
    payload.id = id;
    const promise = new Promise<any>(resolve => {
      this.pending.set(id, resolve);
    });
    this.socket?.send(JSON.stringify(payload));
    return promise;
  }

  dispose() {
    this.socket?.close();
  }
}

import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { API_URL } from "./environment";

export interface User {
  id: string;
  username?: string;
  weight: number;
}

export interface Error {
  code: number;
  message: string;
}

@Injectable({providedIn: "root"})
export class AuthService {
  public user$?: Promise<User>;
  public error$?: Promise<string>;

  constructor(private http: HttpClient) {
    if (typeof document !== "undefined" && document.cookie) {
      const username = document.cookie.split("username=")[1].slice(-1);
      const password = document.cookie.split("password=")[1].slice(-1);

      this.http.post<User | Error>(`${API_URL}/users/login`, {username, password}).subscribe(response => {
        if ((response as Error).code) {
          this.error$ = Promise.resolve((response as Error).message);
          return;
        }

        this.user$ = Promise.resolve(response as User);
      });
    }
  }

  register(username: string, password: string, weight: number){
    this.error$ = undefined;

    this.http.post<User | Error>(`${API_URL}/users/register`, {username, password, weight}).subscribe(response => {
      if ((response as Error).code) {
        this.error$ = Promise.resolve((response as Error).message);
        return;
      }

      this.user$ = Promise.resolve(response as User);
      document.cookie = `username=${username}; password=${password}; expires=Thu, 01 Jan 2099 12:00:00 UTC`;
    });
  }

  login(username: string, password: string) {
    this.error$ = undefined;

    this.http.post<User | Error>(`${API_URL}/users/login`, {username, password}).subscribe(response => {
      if ((response as Error).code) {
        this.error$ = Promise.resolve((response as Error).message);
        return;
      }

      this.user$ = Promise.resolve(response as User);
      document.cookie = `username=${username}; password=${password}; expires=Thu, 01 Jan 2099 12:00:00 UTC`;
    });
  }

  logout(): void {
    this.error$ = undefined;
    this.user$ = undefined;
    document.cookie = `username=; password=; expires=Thu, 01 Jan 2099 12:00:00 UTC`;
  }
}

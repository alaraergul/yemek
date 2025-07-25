import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { API_URL } from "./environment";
import { BehaviorSubject } from "rxjs";

export interface User {
  id: string;
  username?: string;
  weight: number;
};

export interface Error {
  code: number;
  message: string;
};

@Injectable({providedIn: "root"})
export class AuthService {
  public isLogged$: BehaviorSubject<boolean> = new BehaviorSubject(false);
  public user$: Promise<User | null> = Promise.resolve(null);
  public username?: string;
  public error$?: Promise<Error>;

  constructor(private http: HttpClient) {}

  async initialize() {
    return new Promise((resolve) => {
      if (typeof document !== "undefined" && document.cookie) {
        if (!document.cookie.split("username=")[1] || !document.cookie.split("password=")[1]) return resolve(false);

        const username = document.cookie.split("username=")[1].split(";")[0];
        const password = document.cookie.split("password=")[1].split(";")[0];

        if (username == "" || password == "") return resolve(false);

        this.http.post<User | Error>(`${API_URL}/users/login`, {username, password}).subscribe(async (response) => {
          if ((response as Error).code) {
            this.error$ = Promise.resolve((response as Error));
            return;
          }

          this.user$ = Promise.resolve(response as User);
          this.username = username;
          this.isLogged$.next(true);
          resolve(true);
        });
      } else {
        resolve(false);
      }
    });
  }

  register(username: string, password: string, weight: number){
    this.error$ = undefined;

    this.http.post<User | Error>(`${API_URL}/users/register`, {username, password, weight}).subscribe(response => {
      if ((response as Error).code) {
        this.error$ = Promise.resolve(response as Error);
        return;
      }

      this.username = username;
      this.user$ = Promise.resolve(response as User);
      this.isLogged$.next(true);
      document.cookie = `username=${username};expires=Thu, 01 Jan 2099 12:00:00 UTC`;
      document.cookie = `password=${password};expires=Thu, 01 Jan 2099 12:00:00 UTC`;
    });
  }

  login(username: string, password: string) {
    this.error$ = undefined;

    return new Promise((resolve) => {
      this.http.post<User | Error>(`${API_URL}/users/login`, {username, password}).subscribe(response => {
        if ((response as Error).code) {
          this.error$ = Promise.resolve(response as Error);
          return resolve(false);
        }

        this.username = username;
        this.user$ = Promise.resolve(response as User);
        this.isLogged$.next(true);
        document.cookie = `username=${username};expires=Thu, 01 Jan 2099 12:00:00 UTC`;
        document.cookie = `password=${password};expires=Thu, 01 Jan 2099 12:00:00 UTC`;
        return resolve(true);
      });
    });
  }

  logout(): void {
    this.error$ = undefined;
    this.user$ = Promise.resolve(null);
    this.isLogged$.next(false);
    document.cookie = `username=;`;
    document.cookie = `password=;`;
  }
}

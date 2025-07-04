import { Component, inject, OnInit } from "@angular/core";
import { AuthService } from "./auth.service";
import { CommonModule } from "@angular/common";

enum Tabs {
  LOGIN,
  REGISTER
};

@Component({
  templateUrl: "./auth.component.html",
  styleUrl: "./auth.component.css",
  imports: [CommonModule]
})
export class AuthComponent implements OnInit {
  authService = inject(AuthService);

  activeTab: Tabs = Tabs.LOGIN;
  Tabs = Tabs;

  async ngOnInit() {
    await this.authService.initialize();
  }

  login(username: string, password: string) {
    this.authService.login(username, password);
  }

  register(username: string, password: string, weight: number) {
    this.authService.register(username, password, weight);
  }

  logout() {
    this.authService.logout();
  }

  get user$() {
    return this.authService.user$;
  }

  get error$() {
    return this.authService.error$;
  }
}

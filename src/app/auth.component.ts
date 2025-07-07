import { Component, inject, OnInit } from "@angular/core";
import { AuthService } from "./auth.service";
import { CommonModule } from "@angular/common";
import { Router, RouterLink } from "@angular/router";

enum Tabs {
  LOGIN,
  REGISTER
};

@Component({
  templateUrl: "./auth.component.html",
  styleUrl: "./auth.component.css",
  imports: [CommonModule, RouterLink]
})
export class AuthComponent implements OnInit {
  authService = inject(AuthService);

  activeTab: Tabs = Tabs.LOGIN;
  Tabs = Tabs;

  constructor(private router: Router) {}

  async ngOnInit() {
    await this.authService.initialize();
  }

  login(username: string, password: string) {
    this.authService.login(username, password).then(async (result) => {
      if (result) this.router.navigate(["/purin"]);
    });
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

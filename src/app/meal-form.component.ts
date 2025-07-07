import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { Meal, MealEntry, meals, Nullable } from './data';
import { AuthService } from './auth.service';
import { RouterLink } from '@angular/router';
import { Router } from '@angular/router';
import { ChartComponent } from './components/chart.js.component';
import { API_URL } from './environment';

@Component({
  selector: 'app-meal-form',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink, ChartComponent],
  templateUrl: './meal-form.component.html',
  styleUrls: ['./meal-form.component.css']
})
export class MealFormComponent implements OnInit {
  authService = inject(AuthService);

  data$?: Promise<MealEntry[]>;
  today = new Date();
  date = {
    day: this.today.getDate(),
    month: this.today.getMonth(),
    year: this.today.getFullYear()
  };

  currentMealEntry: Nullable<MealEntry> = {
    timestamp: this.today.getTime(),
    count: 1,
    meal: meals[0]
  };

  constructor(private http: HttpClient, private router: Router) { }

  async ngOnInit(): Promise<void> {
    await this.authService.initialize();
    await this.loadEntries();
  }

  createDateFrom(timestamp: number) {
    return new Date(timestamp);
  }

  addZero(value: number) {
    return value.toString().padStart(2, "0")
  }

  get user$() {
    return this.authService.user$;
  }

  async loadEntries(): Promise<void> {
    if (this.authService.isLogged$.getValue()) {
      this.data$ = Promise.resolve([]);

      this.http.get<({ id: number, count: number, timestamp: number })[]>(`${API_URL}/users/${(await this.user$)?.id}`).subscribe((response) => {
        const entries: MealEntry[] = [];

        for (const value of response) {
          entries.push({
            meal: this.getAllMeals().find((meal) => meal.id == value.id) as Meal,
            count: value.count,
            timestamp: value.timestamp
          })
        }

        this.data$ = Promise.resolve(entries);
      });
    }
  }

  async addMeal(): Promise<void> {
    const mealId = this.currentMealEntry.meal?.id;
    const count = this.currentMealEntry.count;
    const timestamp = this.currentMealEntry.timestamp;

    const data = await this.data$ as MealEntry[];
    const exists = data.some(entry => entry.meal.id === mealId && entry.timestamp === timestamp);

    if (exists) {
      alert("Bu kayıt zaten girilmiş.");
      return;
    }

    const body = {
      id: mealId,
      count,
      timestamp
    };

    await fetch(`${API_URL}/users/${(await this.user$)?.id}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body)
    });

    data.push(this.currentMealEntry as MealEntry);
    this.data$ = Promise.resolve(data);

    this.currentMealEntry = {
      timestamp: this.today.getTime(),
      count: 1,
      meal: meals[0]
    };
  }

  async deleteMeal(id: number, timestamp: number): Promise<void> {
    await fetch(`${API_URL}/users/${(await this.user$)?.id}`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({id, timestamp})
    });

    const data = await this.data$ as MealEntry[];
    this.data$ = Promise.resolve(data.filter((entry) => entry.meal.id != id) as MealEntry[]);
  }

  async resetMealsByDate(): Promise<void> {
    const data = await this.data$ as MealEntry[];
    const entriesByDate = this.getEntriesOfDate(data);

    for (const entry of entriesByDate) {
      await fetch(`${API_URL}/users/${(await this.user$)?.id}`, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          id: entry.meal.id,
          timestamp: entry.timestamp
        })
      });
    }

    const mappedById = entriesByDate.map((entry) => entry.meal.id);
    this.data$ = Promise.resolve(data.filter((entry) => !mappedById.includes(entry.meal.id)) as MealEntry[]);
  }

  getAllMeals(): Meal[] {
    return meals;
  }

  getEntriesOfDate(data: MealEntry[]): MealEntry[] {
    return data.filter(entry => {
      const addedAt = new Date(entry.timestamp);
      return addedAt.getDate() == this.date.day && addedAt.getMonth() == this.date.month && addedAt.getFullYear() == this.date.year;
    })
  }

  getTotalPurine(data: MealEntry[]): number {
    return data.reduce((sum, value) => sum + (value.count * value.meal.purine), 0);
  }


  getComment(purineAmount: number): string {
    if (purineAmount < 150) return "Harika! Düşük pürin aldınız.";
    else if (purineAmount < 300) return "İyi gidiyorsunuz ama dikkatli olun.";
    else return "Dikkat! Bugünkü pürin alımı yüksek.";
  }

  onSelectMeal(event: Event): void {
    const mealId = Number((event.target as HTMLSelectElement).value);
    const selected = meals.find(m => m.id === mealId);
    if (selected) this.currentMealEntry.meal = selected;
  }

  getWeeklyPurine(data: MealEntry[]): number {
    const now = new Date();

    const day = now.getDay();
    const diffToMonday = (day === 0 ? -6 : 1) - day;

    const monday = new Date(now);
    monday.setDate(now.getDate() + diffToMonday);
    monday.setHours(0, 0, 0, 0);

    const sunday = new Date(now);
    sunday.setDate(sunday.getDate() + 6);
    sunday.setHours(23, 59, 59, 999);

    const mondayTime = monday.getTime();
    const sundayTime = sunday.getTime();

    const weeklyEntries = data.filter(entry => entry.timestamp >= mondayTime && entry.timestamp <= sundayTime);
    return weeklyEntries.reduce((sum, entry) => sum + (entry.count * entry.meal.purine), 0);

  }

  getWeeklyComment(data: MealEntry[]): string {
    const total = this.getWeeklyPurine(data);
    const limit = 2000;
    if (total <= limit) return "Haftalık pürin alımınız sağlıklı sınırlarda.";
    return `Dikkat! Bu hafta ${total} mg pürin aldınız. Bu miktar önerilen sınırı (${limit} mg) aşıyor.`;
  }

  onTimestampInput(event: Event): void {
    this.currentMealEntry.timestamp = new Date((event.target as HTMLInputElement).value).getTime();
  }

  onDateInput(event: Event): void {
    const date = new Date((event.target as HTMLInputElement).value);
    this.date.day = date.getDate();
    this.date.month = date.getMonth();
    this.date.year = date.getFullYear();
  }

logout(): void {
  this.authService.logout();
  this.router.navigate(['/purin/auth']);
}

}






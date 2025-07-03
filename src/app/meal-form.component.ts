import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { Meal, MealEntry, meals } from './data';

const API_URL = "http://localhost:5000";

@Component({
  selector: 'app-meal-form',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './meal-form.component.html',
  styleUrls: ['./meal-form.component.css']
})
export class MealFormComponent implements OnInit {
  userId: number = 1;
  data$: Promise<MealEntry[]> = Promise.resolve([]);
  todayEntries: MealEntry[] = [];

  currentMealEntry = {
    timestamp: '',
    count: null as number | null,
    meal: null as Meal | null
  };

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    this.loadTodayMeals();
  }

  async loadTodayMeals(): Promise<void> {
    const allEntries = await this.http.get<MealEntry[]>(`${API_URL}/users/${this.userId}`).toPromise() || [];
    const todayStart = new Date();
    todayStart.setHours(0, 0, 0, 0);
    const todayEnd = new Date();
    todayEnd.setHours(23, 59, 59, 999);

    this.todayEntries = allEntries.filter(entry => {
      const ts = typeof entry.timestamp === 'string' ? Number(entry.timestamp) : entry.timestamp;
      return ts >= todayStart.getTime() && ts <= todayEnd.getTime();
    });

    this.data$ = Promise.resolve(this.todayEntries);
  }

  async addMeal(): Promise<void> {
    if (!this.currentMealEntry.meal || this.currentMealEntry.count === null || !this.currentMealEntry.timestamp) {
      alert("Lütfen tüm alanları doldurun.");
      return;
    }

    const mealId = this.currentMealEntry.meal.id;
    const count = this.currentMealEntry.count;
    const tsNumber = new Date(this.currentMealEntry.timestamp).getTime();

    const exists = this.todayEntries.some(entry =>
      entry.id === mealId && Number(entry.timestamp) === tsNumber
    );

    if (exists) {
      alert("Bu kayıt zaten girilmiş.");
      return;
    }

    const body = {
      id: mealId,
      count: count,
      timestamp: tsNumber
    };

    await this.http.post(`${API_URL}/users/${this.userId}`, body).toPromise();
    this.currentMealEntry = { timestamp: '', count: null, meal: null };
    this.loadTodayMeals();
  }

  async resetMeals(): Promise<void> {
    const allEntries = await this.http.get<MealEntry[]>(`${API_URL}/users/${this.userId}`).toPromise() || [];

    const todayStart = new Date();
    todayStart.setHours(0, 0, 0, 0);
    const todayEnd = new Date();
    todayEnd.setHours(23, 59, 59, 999);

    const todayEntries = allEntries.filter(entry => {
      const ts = typeof entry.timestamp === 'string' ? Number(entry.timestamp) : entry.timestamp;
      return ts >= todayStart.getTime() && ts <= todayEnd.getTime();
    });

    for (const entry of todayEntries) {
      await this.http.request('delete', `${API_URL}/users/${this.userId}`, {
        body: {
          id: entry.id,
          timestamp: entry.timestamp
        }
      }).toPromise();
    }

    this.loadTodayMeals();
  }

  getAllMeals(): Meal[] {
    return meals;
  }

  getTotalPurine(data: MealEntry[]): number {
    return data.reduce((total, entry) => {
      const m = meals.find(meal => meal.id === entry.id || meal.id === entry.meal?.id);
      return m ? total + (entry.count * m.purine) : total;
    }, 0);
  }

  getComment(data: MealEntry[]): string {
    const total = this.getTotalPurine(data);
    if (total < 200) return "Harika! Düşük pürin aldınız.";
    else if (total < 400) return "İyi gidiyorsunuz ama dikkatli olun.";
    else return "Dikkat! Bugünkü pürin alımı yüksek.";
  }

  onSelectMeal(event: Event): void {
    const mealId = Number((event.target as HTMLSelectElement).value);
    const selected = meals.find(m => m.id === mealId);
    if (selected) this.currentMealEntry.meal = selected;
  }

  onDateInput(event: Event): void {
    this.currentMealEntry.timestamp = (event.target as HTMLInputElement).value;
  }
}

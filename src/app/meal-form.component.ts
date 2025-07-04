import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { Meal, MealEntry, meals, Nullable } from './data';

const API_URL = "http://localhost:5000";

@Component({
  selector: 'app-meal-form',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './meal-form.component.html',
  styleUrls: ['./meal-form.component.css']
})
export class MealFormComponent implements OnInit {
  userId: Promise<number | null> = Promise.resolve(null);
  data$: Promise<MealEntry[]> = Promise.resolve([]);
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

  constructor(private http: HttpClient) {}

  async ngOnInit(): Promise<void> {
    await this.loadId();
    await this.loadEntries();
  }

  createDateFrom(timestamp: number) {
    return new Date(timestamp);
  }

  addZero(value: number) {
    return value.toString().padStart(2, "0")
  }

  async loadId(): Promise<void> {
    let id = localStorage.getItem("id");

    if (id) {
      this.userId = Promise.resolve(parseInt(id));
      return;
    }

    this.http.get<string[]>(`${API_URL}/users`).subscribe(response => {
      const res = response.map((value) => parseInt(value));
      let value;

      do {
        value = Math.floor(Math.random() * 10000);
      } while (res.includes(value));

      id = value.toString();
      localStorage.setItem("id", id);
      this.userId = Promise.resolve(value);
    });
  }

  async loadEntries(): Promise<void> {
    this.http.get<({id: number, count: number, timestamp: number})[]>(`${API_URL}/users/${await this.userId}`).subscribe((response) => {
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

  async addMeal(): Promise<void> {
    const mealId = this.currentMealEntry.meal?.id;
    const count = this.currentMealEntry.count;
    const timestamp = this.currentMealEntry.timestamp;

    const data = await this.data$;
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

    await fetch(`${API_URL}/users/${await this.userId}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body)
    });

    data.push(this.currentMealEntry as MealEntry);
    this.data$ = Promise.resolve(data);

    this.currentMealEntry = {
      timestamp: null,
      count: null,
      meal: null
    };
  }

  async resetMealsByDate(): Promise<void> {
    const data = await this.data$;
    const entriesByDate = this.getEntriesOfDate(data);

    for (const entry of entriesByDate) {
      await fetch(`${API_URL}/users/${await this.userId}`, {
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
    return data.reduce((total, entry) => {
      const m = meals.find(meal => meal.id === entry.meal.id || meal.id === entry.meal?.id);
      return m ? total + (entry.count * m.purine) : total;
    }, 0);
  }

  getComment(purineAmount: number): string {
    if (purineAmount < 200) return "Harika! Düşük pürin aldınız.";
    else if (purineAmount < 400) return "İyi gidiyorsunuz ama dikkatli olun.";
    else return "Dikkat! Bugünkü pürin alımı yüksek.";
  }

  onSelectMeal(event: Event): void {
    const mealId = Number((event.target as HTMLSelectElement).value);
    const selected = meals.find(m => m.id === mealId);
    if (selected) this.currentMealEntry.meal = selected;
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
}

import { Component, OnInit } from '@angular/core';
import { Meal, meals } from './data';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { MealFormComponent } from './meal-form.component';


interface MealEntry {
  meal: Meal;
  count: number;
  timestamp: number;
};

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [ MealFormComponent, MealFormComponent],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App implements OnInit {
  public data$: Promise<MealEntry[] | null> = Promise.resolve(null);

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    // will be fetched all MealEntries from database via backend API
    // we need to determine ID values for all clients/website users

    /*
      this.http.get(`{API_URL}/users/${this.userId}`).subscribe((response) => {
        this.data$ = Promise.resolve(response as MealEntry[]);
      });
    */
  }

  public getTotalOfPurine(data: MealEntry[]): number {
    return data.reduce((sum, value) => sum + (value.count * value.meal.purine), 0);
  }

  public addMealEntry(mealId: string, count: number, timestamp: number) {
    // will be posted to database via backend API

    /*
      this.http.post(`{API_URL}/users/${this.userId}`, {
        id: mealId,
        count,
        timestamp
      }).subscribe(async (response) => {
        const mealEntry = response as MealEntry;
        const data = await this.data$;
        data?.push(mealEntry);

        this.data$ = Promise.resolve(data);
      });
    */
  }

  public deleteMealEntry(mealId: string, timestamp: number) {
    // will be deleted from database via backend API

    /*
      this.http.post(`{API_URL}/users/${this.userId}`, {
        id: mealId,
        timestamp
      }).subscribe(async (response) => {
        const mealEntry = response as MealEntry;
        const data = await this.data$;
        data?.push(mealEntry);

        this.data$ = Promise.resolve(data);
      });
    */
  }

  public getAllMeals(): Meal[] {
    return meals;
  }
}

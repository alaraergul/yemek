import { ChangeDetectorRef, Component, Input, OnChanges, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BaseChartDirective } from 'ng2-charts';
import { ChartConfiguration, ChartOptions, ChartType } from 'chart.js';
import { MealEntry } from '../data';

@Component({
  selector: 'app-chart',
  standalone: true,
  imports: [CommonModule, BaseChartDirective],
  template: `
    <div style="width: 80%; max-width: 400px; height: 300px; margin: auto;">
  <canvas baseChart
    [type]="'line'"
    [data]="lineChartData"
    [options]="lineChartOptions"
    [legend]="lineChartLegend">
  </canvas>
</div>

  `
})
export class ChartComponent implements OnInit {
  @Input("data") data: Promise<MealEntry[]> | undefined;

  public lineChartData: ChartConfiguration<"line">["data"] = {
    labels: [
      "Pazartesi",
      "Salı",
      "Çarşamba",
      "Perşembe",
      "Cuma",
      "Cumartesi",
      "Pazar"
    ],
    datasets: [
      {
        data: [],
        label: 'Series A',
        fill: true,
        tension: 0.5,
        borderColor: 'black',
        backgroundColor: 'rgba(255,0,0,0.3)'
      }
    ]
  };

  public lineChartOptions: ChartOptions<'line'> = {
    responsive: true,
    maintainAspectRatio: false
  };

  public lineChartLegend = false;

  async ngOnInit(): Promise<void> {
    const data = await this.data;
    const now = new Date();
    const day = now.getDay();
    const diffToMonday = (day === 0 ? -6 : 1) - day;

    const monday = new Date(now);
    monday.setDate(now.getDate() + diffToMonday);
    monday.setHours(0, 0, 0, 0);

    const sunday = new Date(now);
    sunday.setDate(sunday.getDate() + 6);
    monday.setHours(23, 59, 59, 999);

    if (data) {
      const days = Array(7).fill(0);
      const _data = data.filter((entry) => monday.getTime() <= entry.timestamp && entry.timestamp <= sunday.getTime());

      for (const entry of _data) {
        const value = new Date(entry.timestamp);

        days[value.getDay()] += entry.meal.purine * entry.count;
      }

      this.lineChartData = {
        ...this.lineChartData,
        datasets: [
          {
            data: days
          }
        ]
      };
    }
  }
}

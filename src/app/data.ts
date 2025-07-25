export type Nullable<T> = {
  [P in keyof T]: T[P] | null;
};

export interface MealEntry {
  meal: Meal;
  count: number;
  timestamp: number;
};

export interface Meal {
  id: number;
  name: string;
  purine: number; // mg
  quantity: number; // g
  kcal: number;
  sugar: number; // g
}

export const meals: Meal[] = [
  { id: 1, name: "Beyaz Ekmek", purine: 12, quantity: 100, kcal: 265, sugar: 5 },
  { id: 2, name: "Tam Buğday Ekmeği", purine: 13, quantity: 100, kcal: 247, sugar: 4.3 },
  { id: 3, name: "Simit", purine: 22, quantity: 100, kcal: 295, sugar: 3 },
  { id: 4, name: "Pide", purine: 15, quantity: 100, kcal: 262, sugar: 2.5 },
  { id: 5, name: "Lavaş", purine: 12, quantity: 100, kcal: 305, sugar: 2 },
  { id: 6, name: "Pirinç (pişmiş)", purine: 5, quantity: 100, kcal: 130, sugar: 0.1 },
  { id: 7, name: "Bulgur (pişmiş)", purine: 10, quantity: 100, kcal: 120, sugar: 0.2 },
  { id: 8, name: "Makarna (pişmiş)", purine: 16, quantity: 100, kcal: 131, sugar: 0.6 },
  { id: 9, name: "Sığır Eti (pişmiş)", purine: 120, quantity: 100, kcal: 250, sugar: 0 },
  { id: 10, name: "Kuzu Eti (pişmiş)", purine: 130, quantity: 100, kcal: 294, sugar: 0 },
  { id: 11, name: "Tavuk Göğsü (pişmiş)", purine: 175, quantity: 100, kcal: 165, sugar: 0 },
  { id: 12, name: "Hindi Eti (pişmiş)", purine: 150, quantity: 100, kcal: 189, sugar: 0 },
  { id: 13, name: "Hamsi", purine: 305, quantity: 100, kcal: 210, sugar: 0 },
  { id: 14, name: "Sardalya (konserve)", purine: 345, quantity: 100, kcal: 208, sugar: 0 },
  { id: 15, name: "Somon", purine: 170, quantity: 100, kcal: 208, sugar: 0 },
  { id: 16, name: "Sucuk", purine: 110, quantity: 100, kcal: 455, sugar: 0 },
  { id: 17, name: "Salam", purine: 90, quantity: 100, kcal: 420, sugar: 0 },
  { id: 18, name: "Pastırma", purine: 125, quantity: 100, kcal: 450, sugar: 0 },
  { id: 19, name: "Yumurta", purine: 10, quantity: 100, kcal: 155, sugar: 1.1 },
  { id: 20, name: "Süt (yağlı)", purine: 0, quantity: 100, kcal: 61, sugar: 5 },
  { id: 21, name: "Laktozsuz Süt", purine: 0, quantity: 100, kcal: 50, sugar: 3 },
  { id: 22, name: "Yoğurt (tam yağlı)", purine: 7, quantity: 100, kcal: 59, sugar: 3.2 },
  { id: 23, name: "Ayran", purine: 0, quantity: 100, kcal: 37, sugar: 1.5 },
  { id: 24, name: "Beyaz Peynir", purine: 7, quantity: 100, kcal: 260, sugar: 0.5 },
  { id: 25, name: "Kaşar Peyniri", purine: 8, quantity: 100, kcal: 404, sugar: 0.5 },
  { id: 26, name: "Domates", purine: 5, quantity: 100, kcal: 18, sugar: 2.6 },
  { id: 27, name: "Salatalık", purine: 7, quantity: 100, kcal: 16, sugar: 1.7 },
  { id: 28, name: "Havuç", purine: 17, quantity: 100, kcal: 41, sugar: 4.7 },
  { id: 29, name: "Ispanak (pişmiş)", purine: 57, quantity: 100, kcal: 23, sugar: 0.4 },
  { id: 30, name: "Brokoli (haşlanmış)", purine: 70, quantity: 100, kcal: 35, sugar: 1.7 },
  { id: 31, name: "Lahana", purine: 15, quantity: 100, kcal: 25, sugar: 3.2 },
  { id: 32, name: "Soğan", purine: 8, quantity: 100, kcal: 40, sugar: 4.2 },
  { id: 33, name: "Sarımsak", purine: 12, quantity: 100, kcal: 149, sugar: 1 },
  { id: 34, name: "Patates (haşlanmış)", purine: 15, quantity: 100, kcal: 87, sugar: 0.8 },
  { id: 35, name: "Elma", purine: 14, quantity: 100, kcal: 52, sugar: 10 },
  { id: 36, name: "Muz", purine: 57, quantity: 100, kcal: 89, sugar: 12 },
  { id: 37, name: "Portakal", purine: 19, quantity: 100, kcal: 47, sugar: 9 },
  { id: 38, name: "Karpuz", purine: 7, quantity: 100, kcal: 30, sugar: 6 },
  { id: 39, name: "Kavun", purine: 8, quantity: 100, kcal: 34, sugar: 7.9 },
  { id: 40, name: "Üzüm (siyah)", purine: 27, quantity: 100, kcal: 69, sugar: 15 },
  { id: 41, name: "Çilek", purine: 13, quantity: 100, kcal: 32, sugar: 4.9 },
  { id: 42, name: "Kayısı", purine: 10, quantity: 100, kcal: 48, sugar: 9 },
  { id: 43, name: "Mercimek (pişmiş)", purine: 50, quantity: 100, kcal: 116, sugar: 1.8 },
  { id: 44, name: "Nohut (pişmiş)", purine: 40, quantity: 100, kcal: 164, sugar: 2.2 },
  { id: 45, name: "Kuru Fasulye (pişmiş)", purine: 45, quantity: 100, kcal: 127, sugar: 0.3 },
  { id: 46, name: "Barbunya (pişmiş)", purine: 50, quantity: 100, kcal: 100, sugar: 0.5 },
  { id: 47, name: "Soya Fasulyesi", purine: 190, quantity: 100, kcal: 173, sugar: 3 },
  { id: 48, name: "Ceviz", purine: 25, quantity: 100, kcal: 654, sugar: 2.6 },
  { id: 49, name: "Badem", purine: 10, quantity: 100, kcal: 579, sugar: 4.4 },
  { id: 50, name: "Fındık", purine: 10, quantity: 100, kcal: 628, sugar: 4.3 },
  { id: 51, name: "Ayçekirdeği", purine: 65, quantity: 100, kcal: 584, sugar: 2.6 },
  { id: 52, name: "Kabak çekirdeği", purine: 40, quantity: 100, kcal: 559, sugar: 1.4 },
  { id: 53, name: "Bal", purine: 0, quantity: 100, kcal: 304, sugar: 82 },
  { id: 54, name: "Reçel", purine: 0, quantity: 100, kcal: 278, sugar: 60 },
  { id: 55, name: "Sütlü Çikolata", purine: 20, quantity: 100, kcal: 535, sugar: 50 },
  { id: 56, name: "Bitter Çikolata", purine: 25, quantity: 100, kcal: 546, sugar: 24 },
  { id: 57, name: "Lokum", purine: 0, quantity: 100, kcal: 325, sugar: 80 },
  { id: 58, name: "Dondurma (vanilya)", purine: 7, quantity: 100, kcal: 207, sugar: 21 },
  { id: 59, name: "Kek (hazır)", purine: 10, quantity: 100, kcal: 390, sugar: 30 },
  { id: 60, name: "Kola (330 ml)", purine: 0, quantity: 330, kcal: 139, sugar: 35 },
  { id: 61, name: "Portakal suyu", purine: 0, quantity: 100, kcal: 45, sugar: 8 },
  { id: 62, name: "Meyveli Soda", purine: 0, quantity: 100, kcal: 25, sugar: 5 },
  { id: 63, name: "Enerji İçeceği", purine: 0, quantity: 100, kcal: 110, sugar: 27 },
  { id: 64, name: "Zeytin", purine: 29, quantity: 100, kcal: 105, sugar: 0 },
  { id: 65, name: "Lahmacun", purine: 250, quantity: 100, kcal: 462, sugar: 4 },
  { id: 66, name: "Sosis", purine: 100, quantity: 100, kcal: 300, sugar: 1 },
  { id: 67, name: "Mandalina", purine: 1.7, quantity: 100, kcal: 47, sugar: 9 },
  { id: 68, name: "Zeytinyağlı Yaprak Sarma", purine: 35, quantity: 100, kcal: 32, sugar: 1 },
  { id: 69, name: "Zeytinyağlı Taze Fasulye", purine: 7.4, quantity: 100, kcal: 73, sugar: 1.5 },
  { id: 70, name: "Yayla Çorbası", purine: 32.5, quantity: 100, kcal: 175, sugar: 2.5 },
  { id: 71, name: "Ton balığı", purine: 290, quantity: 100, kcal: 160, sugar: 0 },
  { id: 72, name: "Karnabahar (haşlanmış)", purine: 57, quantity: 100, kcal: 25, sugar: 1.9 },
  { id: 73, name: "Kuşkonmaz", purine: 65, quantity: 100, kcal: 20, sugar: 1.9 },
  { id: 74, name: "Yeşil Biber", purine: 70, quantity: 100, kcal: 20, sugar: 2.4 },
  { id: 75, name: "Labne", purine: 6, quantity: 100, kcal: 240, sugar: 2.4 }
];


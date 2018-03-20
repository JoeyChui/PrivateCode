package com.company;

import java.util.ArrayList;
import java.util.Iterator;

class Hero {
    String name;
    Hero(String str) {
        name = str;
    }
}


public class Main {
      public static void main(String[] args) {
          ArrayList heros = new ArrayList();
          Iterator<Hero> it= heros.iterator();

          // 初始化5个对象
          for (int i = 0; i < 5; i++) {
              heros.add(new Hero("hero " + i));
          }
          System.out.println(heros);

          Hero hs[] = (Hero[])heros.toArray(new Hero[]{});
          System.out.println("数组:" +hs);
          System.out.println(hs.length);
      }
}

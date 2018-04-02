package com.company;

import java.util.*;
import java.util.Collections;

class Hero implements Runnable{
    String name;
    Hero(String str) {
        name = str;
    }
    void fun() {
        int fun = 8;
    }
}


public class Main {
    public static void main(String[] args) {
        int lengh = 1000;
        int[] numbers = new int[lengh];
        for (int num : numbers) {
            num = (int)(Math.random() * 1000) + 100;
        }
        for (int num : numbers) {
            System.out.println(num);
        }
        System.out.println(numbers);
        Hero hero = new Hero("");
        HashSet hs = new HashSet();
        hs.add(hero);
        boolean result = hs.add(hero);
        System.out.println(hs);
        System.out.println(result);
        Collections.swap(numbers);
        Hero.getClass();

    }
}


public class LinkedList {

    private class Data{
        private Object obj;
        private Data next = null;

        Data(Object obj){
            this.obj = obj;
        }
    }

    private Data first = null;

    public void insertFirst(Object obj){
        Data data = new Data(obj);
        data.next = first;
        first = data;
    }

    public Object deleteFirst() throws Exception{
        if(first == null)
            throw new Exception("empty!");
        Data temp = first;
        first = first.next;
        return temp.obj;
    }

    public Object find(Object obj) throws Exception{
        if(first == null)
            throw new Exception("LinkedList is empty!");

        Data cur = first;
        while(cur != null){
            if(cur.obj.equals(obj)){
                return cur.obj;
            }
            cur = cur.next;
        }
        return null;
    }

    public void remove(Object obj) throws Exception{
        if(first == null)
            throw new Exception("LinkedList is empty!");
        if(first.obj.equals(obj)){
            first = first.next;
        }else{
            Data pre = first;
            Data cur = first.next;
            while(cur != null){
                if(cur.obj.equals(obj)){
                    pre.next = cur.next;
                }
                pre = cur;
                cur = cur.next;
            }
        }
    }

    public boolean isEmpty(){
        return (first == null);
    }

    public void display(){
        if(first == null)
            System.out.println("empty");

        Data cur = first;

        while(cur != null){
            System.out.print(cur.obj.toString() + " -> ");
            cur = cur.next;
        }

        System.out.print("\n");
    }

    public static void main(String[] args) throws Exception {
        LinkedList ll = new LinkedList();
        ll.insertFirst(4);
        ll.insertFirst(3);
        ll.insertFirst("sdfgh");
        ll.insertFirst(1);
        ll.display();
        ll.deleteFirst();
        ll.display();
        ll.remove(3);
        ll.display();
        System.out.println(ll.find(1));
        System.out.println(ll.find(4));
    }

}


链接：https://www.nowcoder.com/questionTerminal/a174820de48147d489f64103af152709
来源：牛客网

//这个题目其实非常简单，只要考虑两个条件，第一，总数一定能被牛的数量整除，第二，每头牛
//比平均值多出来的苹果数一定能被2整除，不满足这两个条件的输出-1，满足的情况下，将比平均值
//多出的苹果数除2，就是移动次数
import java.util.Arrays;
import java.util.Scanner;
 
/**
 * Created by 梅晨 on 2017/9/13.
 */
public class Main {
    public static void main(String[] args){
        Scanner in = new Scanner(System.in);
        while (in.hasNext()){
            int num = in.nextInt();
            int[] apples = new int[num];
            int sum = 0;
            for(int i = 0; i < num; i++){
                int a = in.nextInt();
                sum += a;
                apples[i] = a;
            }
            int avg = sum / num;
            if(sum % num != 0){
                System.out.println(-1);
                return;
            }
            int res = 0;
            for(int n : apples){
                if(n > avg){
                    int over = n - avg;
                    if(over % 2 != 0){
                        System.out.print(-1);
                        return;
                    }else {
                        res += over / 2;
                    }
                }
            }
            System.out.println(res);
        }
    }
}


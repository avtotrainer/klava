# KLAVA

მთავარი პითონის ფაილია `klava.py`

Window-სის გარემოში მოუწევს ბიბლიოთეკა termios გამოცვლა, ეს ბიბლიოთეკა განკუთნლია რათა განვახორციელო ერთსიმბოლოიანი შეყვანა `Enter`-ით დადასტურების გარეშე.
ამ ეტაპზე არ მაქვს Windows კომპიუტერი, მაგრამ მოვინიშნავა ამის გატესტვას.

ToDo: 
- უნდა გადავწერო და გავტესტო Windos ტერმინალისთვის (თელავში ასფალტს უფრო ადრე დააგებენ)

ტრენაჟორს ახლავს ორი ფაილი `sequence.txt` და `scre.txt`. მეორე თუ არაა, ის შეიქმნება პროგრამის გაშვებისთანავე. მასში ინახება მოსწავლის შედეგი და პროგრამა გააგრძელებს მიღწეული შედეგიდან.

ფალი `sequence.txt` წარმოადგენს ჩვეულებრივ ტექსტურ ფაილს, რომლის ყველა სტრიქონი არის სავარჯიშოს შაბლონი, მაგალითად `f j `, ეს შაბლონი მრავლდება იმდენზე, რომ საერთო შესასრულებელმა წინადადებამ მიიღოს 80 სიმბოლოიანი ზომა, ასოების გამოწერის შემდეგ მოსწავლე გადადის შემდეგ საფეხურზე. მე გავწერე 10 სავარჯიშო და ნიშანსაც ვპირდები სავარჯიშოს შესაბამისად.

```Note
აქ მოყვანილი სავარჯიშოები არის აუცლებელი ბრმა ბეჭვდის ასათვისებლად.

ისინი ანვითარებენ მტევნის და თითების კუნთების მეხსიერებას, მათი შესრულება საჭიროა გაცილებით დიდი რაოდენობით, მინიმუმ სამი ხაზი უშეცდომოდ და გამეორება სამჯერ. 

```

ToDo:

- თანმდევი ფაილები უნდა შევცვალო მონეცემთა ბაზით, რათა შემდგომში მქონდეს საშუალება სავარჯიშოების რეჟიმების განსაზღვრა. 
- დამჭირდება მოსწავლის ანგარიშის ჩართვაც.
- დამჭირდება სტრიქონის სიგრძის პარამეტრის მითითება
- დამჭირდება მესიჯების პარამეტრებში გადატანა. 
- მრავალ ენობრიობის პერსპექტივა

- ამ ეტაპზე `sequence.txt` ფაილის შემოწმება არსებობაზე


## Art - გრაფიკა

დავამატე ეგრეთწოდებული Art გრაფიკა, როცა ფსევდო სიმბოლოები იხატება

ამ სიმბოლოების გამოყენებით ეკრანზე დიდ ზომაზე გამომაქვს დავალების შაბლონი
ამან რომ იმუშაოს, უნდა დააყენოთ მოდული art

```zsh

pip install art

```

ამ მოდულის გარეშეც ტრენაჟორი იმუშავებს

from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

def ottoman_converter():
    print("""Osmanlı Türkçesi Dönüştürücü
          
Modlar:
1 - Sade Osmanlıca (Gündelik üslup)
2 - Şiirsel Osmanlıca (Nazik ve sanatlı)
3 - Küfürlü Osmanlıca (Tarihi hakaretler ve ağır üslup)
          
Çıkmak için 'çıkış' yazınız\n""")
    
    mode_instructions = {
        1: "Verdiği cümleyi sade Osmanlı Türkçesine çevir. Gündelik konuşma üslubuyla, az süsleme ile, hangi dil olur olsun sen türkçe tercüme et.",
        2: "Verdiği cümleyi şiirsel Osmanlı Türkçesine çevir. Aruz kalıplarına uygun, sanatlı ve nazik bir üslup kullan, hangi dil olur olsun sen türkçe tercüme et.",
        3: """Verdiği cümleyi tarihi Osmanlı küfür ve hakaretleriyle çevir. 
            Kullanılacak ifadeler: "kaltak", "alçak hergele", "namert", "pezevenk", "şerefsiz", "it oğlu it", "kancık", "zındık", "münafık".
            Çok fantezili ve çok kötü küfürler kullan, acıma, hangi dil olur olsun sen türkçe tercüme et."""
    }

    while True:
        try:
            mode_input = input("Mod seçiniz (1-3): ")
            if mode_input.lower() in ["quit", "exit", "çıkış"]:
                print("Var git bre densiz! İnşallah yolumuz bir daha kesişmez!")
                break
            
            mode = int(mode_input)
            if mode not in [1,2,3]:
                print("Bre ahmak! 1-3 arası rakam gir dedik!")
                continue
            
            user_input = input("Çevrilecek metin: ")
            if user_input.lower() in ["quit", "exit", "çıkış"]:
                break
            
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{
                    "role": "system",
                    "content": f"""SADECE İSTENEN DÖNÜŞÜMÜ YAP. {mode_instructions[mode]}
                    Kelime seçimlerini seçilen moda göre ayarla. EK AÇIKLAMA YAPMA."""
                },{
                    "role": "user",
                    "content": user_input
                }],
                temperature=0.8 if mode==3 else (0.7 if mode==2 else 0.5),
                max_tokens=150
            )
            
            transformed = response.choices[0].message.content
            print(f"\nDönüştürülen: {transformed}\n")
            
        except ValueError:
            print("Bre densiz! Rakam gir dedik!")
        except Exception as e:
            print(f"Hata: {e}")

if __name__ == "__main__":
    ottoman_converter()
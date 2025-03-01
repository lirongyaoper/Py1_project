magicians = ['alice','david','carolina']
for magician in magicians:
    print(magician)

magicians1 = ['alice','david','carolina']
for magician in magicians1:
    print(f"{magician.title()},that was a great trick!")
print("***********************************************************")
print("在 for 循环结束后执行一些操作:")
magicians = ['alice', 'david', 'carolina']
for magician in magicians:
    print(f"{magician.title()}, that was a great trick!")
    print(f"I can't wait to see your next trick, {magician.title()}.\n")

print("Thank you, everyone. That was a great magic show!")
print("***********************************************************")
from discord.ext import commands
import json
from github import Github, InputGitAuthor

class Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.file = 'ranking/rankings.json'

    #     self.g = Github('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')
    #     self.repo = self.g.get_repo('nanduuuseee/testbot-discord')

    #     self.repo_file = self.repo.get_contents(self.file, ref='main')
    #     self.data = self.repo_file.decoded_content.decode('utf-8')

    # def push(self, path, message, content, branch, update=False):
    #     author = InputGitAuthor('nandoooseee', 'nandagopalnmenon@gmail.com')
    #     source = self.repo.get_branch('main')

    #     # self.repo.create_git_ref(ref=f"refs/heads/{branch}", sha=source.commit.sha)
    #     if update:
    #         contents = self.repo.get_contents(path, ref=branch)
    #         self.repo.delete_file(contents.path, 'Update Json - Delete', contents.sha)
    #         self.repo.create_file(path, 'Update Json - Create', path)
    #     else:
    #         self.repo.create_file(path, message, content, branch=branch, author=author)

    @commands.Cog.listener()
    @commands.guild_only()
    async def on_message(self, message):
        guild = str(message.guild.id)
        author = message.author

        if message.author.bot:
            return

        with open(self.file, 'r') as f:
            data = json.load(f)
        
        if guild in data:
            if str(author.id) in data[guild]:
                data[guild][str(author.id)]['name'] = author.name
                data[guild][str(author.id)]['score'] += 1
            elif str(author.id) not in data[guild]:
                data[guild][str(author.id)] = {
                    'name' : author.name,
                    'score' : 0
                }

        elif guild not in data:
            data[guild] = {
                str(author.id) : {
                    'name' : author.name,
                    'score' : 0
                }
            }

        

        with open(self.file, 'w') as f:
            json.dump(data, f)

        g = Github('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')

        repo = g.get_repo('nandoooseee/testbot-discord')

        content = repo.get_contents(self.file, ref='main')

        repo.delete_file(self.file, 'Updating Json - 1', content.sha)
        repo.create_file(self.file, 'Updating Json - 2', self.file)

        # self.push(self.file, 'Json Updated.', self.data, 'main', update=True)
        print(data)



def setup(bot):
    bot.add_cog(Cog(bot))
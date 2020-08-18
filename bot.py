import discord
from discord.ext import commands
from googlesearch import search
from settings import ES_INDEX, ES_INDEX_MAPPING, ES_INDEX_SETTINGS
from utils import get_es_client, create_elastic_index, get_elasticsearch_doc, \
    write_to_elasticsearch, get_documents_from_elasticsearch

client = commands.Bot(command_prefix='!')


@client.event
async def on_ready():
    es = get_es_client()
    if not es.indices.exists(index=ES_INDEX):
        create_elastic_index(es, ES_INDEX, ES_INDEX_SETTINGS, ES_INDEX_MAPPING)
    print('Bot is ready !!!')


@client.event
async def on_member_join(member):
    print('{} member has joined a server'.format(member))


@client.event
async def on_member_remove(member):
    print('{} member has left a server'.format(member))


@client.event
async def on_message(message):
    if message.content.lower() == "hi":
        channel = message.channel
        await channel.send('hey')
    await client.process_commands(message)


@client.command()
async def ping(ctx):
    """
    command to check latency and if you are able to ping to a bot
    :param ctx: context
    :return:
    """
    await ctx.send('ping and latency is {}'.format(client.latency))


@client.command()
async def google(ctx, *, query=""):
    """
    command to use google search
    :param ctx: context
    :param query: what you want to search
    :return: top 5 search result
    """
    doc = get_elasticsearch_doc(query, ctx.message.author.id)
    # db used is small so resposne might take time
    # can check resp for failure log it and implement a retry mechanism
    resp = write_to_elasticsearch(ES_INDEX, doc)
    for result in search(query, tld="com", num=5, stop=5, pause=1):
        await ctx.send(result)


@client.command()
async def recent(ctx, *, query):
    """
    return queries on which google search was made by as user orderd by time
    in ascending order
    :param ctx: context
    :param query: query for which results needs to be fetched
    :return:
    """
    resp = get_documents_from_elasticsearch(ES_INDEX, query,
                                            ctx.message.author.id)
    if resp.get('exception'):
        await ctx.send(resp.get('exception'))
        return
    for doc in resp.get('hits', {}).get('hits'):
        await ctx.send(doc.get('_source', {}).get('query'))


# cannot keep token here as this is a public repo and discord changes it
# immediately if they find out that token has been compromised
client.run('')


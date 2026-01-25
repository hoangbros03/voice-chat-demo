from agents.graph_builder import get_compiled_graph
import asyncio
import sys

# ignore: noqa
sys.path.append('/workspaces/voice-chat-demo/services/fastrtc_core')


async def main():
    graph = get_compiled_graph()

    query = 'Search best people in VN?'

    initial_state = {
        'messages': [{'role': 'user', 'content': query}],
        'needs_search': False,
        'search_reason': '',
        'search_results': {},
    }

    config = {'configurable': {'thread_id': 'test-thread'}}

    result = await graph.ainvoke(initial_state, config)

    print('Final state:')
    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == '__main__':
    asyncio.run(main())

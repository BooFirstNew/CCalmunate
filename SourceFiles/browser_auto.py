from playwright.sync_api import sync_playwright
import graph_menu.graph_menu
import threading
import graph_menu.utils_helpers
from data.data_accounts import ACCOUNTS_DOLPHIN, ACCOUNTS_ADS, ACCOUNTS_INCOGNITION
from helpers.anty_browser import AntyBrowserAccount, get_initial_data_for_browser
from helpers.metamask import MetamaskAccount
from helpers.telegram_action import send_file_to_telegram, run_async_code_in_thread
from menu import Menu
from projects import spaseFi
from projects.debank.debank import DebankActions
from projects.dmail.dmail import Dmail
from projects.freeactivities.free_activities import Free_activities
from projects.maverik.maverik import MaverikWork
from projects.snapshotActions.snapshotVote import SnapshotVote
from projects.spaseFi.spacefi import SpaseFiWork
from projects.syncswapActions.syncswap import SyncswapWork
from settings import CANCEL, MAX_PERCENTAGE_OF_BALACE, MIX_PERCENTAGE_OF_BALACE, URL_SNAPSHOT, STR_DONE, URL_DEBANK, \
    URL_DMAIL, FILE_TO_TELEGRAM
from utils.token_name import TokenName
from utils.working_with_dir_and_files import create_dir, delete_all_files_in_dir
from data.chain_id import ChainName
from graph_menu import graph_menu
import logging
from web3works.web3_works import get_wallet_balance, gas_is_less_then_MAXGASPRICE, get_token_balance

logging.basicConfig(filename='logs/program.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S', encoding='utf-8')
START_TRHREAD = 0
STOP_TREAD = 0

if __name__ == '__main__':
    # Запустить главный цикл
    graph_menu.window.mainloop()


def start_working(start_browser_mode,
                  browser_type,  # норм / фоновый , долфин/адс
                  selected_profiles,  # передаем выборанные профили
                  name_action,  # передаем выбранное действией
                  gas_limit,  # лимит газа
                  snap_project_name,  # имя проекта в снепшот, в которых будем голосовать
                  debank_type_parsing=None,
                  input_field_posts=None,
                  end_input_filed_post=None,
                  file_name_for_join_draw=None,
                  selectet_chan_for_dmail=None,
                  selecter_free_activities=None,
                  progress_bar=None):
    # get_token_balance("0x2b1aEf40A181cD7c33c58D6238CD90949794c54b", ChainName.ZkSynk, TokenName.UDSD)
    logging.info(f'{START_TRHREAD}   {STOP_TREAD}')

    flag = False
    # stop_thread_parsing - переменная смотртит нужно ли остановить поток и закрыть профиль
    if not graph_menu.stop_thread_parsing:
        if gas_is_less_then_MAXGASPRICE(gas_limit):
            # получяаем параметры для подключения к браузеру
            data_browser_account, str_connect_browser = get_initial_data_for_browser(browser_type)

            # Проверяем тип selected_profiles- должен быть список
            if not isinstance(selected_profiles, list):
                # Если не является списком, преобразуем в список
                selected_profiles = [selected_profiles]

            # Делаем для всех профилей которые введены в файл данных(каждому профилю свой ММ)
            for profile_id in selected_profiles:
                # кошелек с которым будем работать, читаем из файла с профилями
                walletPassword = str(data_browser_account[profile_id]['password']).strip()
                public_key = str(data_browser_account[profile_id]['publickey']).strip()

                # инициализиурем класс для работы с долфин аккаунтом
                antybrowseraccount = AntyBrowserAccount(profile_id, browser_type, start_browser_mode)
                port_ws_endpoint = antybrowseraccount.get_Response_from_DolphinAccount()

                # Подключаемся к запущенному профилю долфина и выполняем автоматизированные действия
                if port_ws_endpoint is not None:
                    with sync_playwright() as p:
                        browser = p.chromium.connect_over_cdp(
                            str_connect_browser + port_ws_endpoint,
                        )
                        # Тут основная логика программы ->
                        # Тут основная логика программы ->
                        # Тут основная логика программы ->

                        # инициализиурем класс метамаска
                        metamask_wallet = MetamaskAccount(browser, public_key, browser_type)

                        # login in metamask проверяем нужно ли логиниться на сайт при помощи кошелька
                        if flag:
                            metamask_wallet.login_in_wallet_account(walletPassword)

                        #  создаем дирикторию с названием кошелька, туда будут скидываться логи
                        root_dir = create_dir(public_key)

                        # и вы вывбераем какое действие выполнять, в соответствии с тем что передает нам graph_menu
                        if name_action == 'debank_parsing':
                            # создаем папку где будут храниться файлы для голосований
                            create_dir('luckydraw')
                            # удаляем все старые голосоваяния
                            # delete_all_files_in_dir('logs/luckydraw')

                            if flag:
                                metamask_wallet.connect_wallet_to_site(URL_DEBANK, 'Log in via web3 wallet', 'metamask')

                            debank = DebankActions(browser, 'metamask_wallet', 'public_key', browser_type)

                            if debank_type_parsing == 'Прямой':
                                debank.pasring_from_start_post_today_to_end(str(input_field_posts),
                                                                            end_input_filed_post, profile_id,progress_bar)

                                if START_TRHREAD == STOP_TREAD:  # Значит завершены все потоки
                                    logging.info(f'{STR_DONE} Все потоки завершены >> отправляем в телеграм')
                                    # Запускаем ваш код в отдельном потоке - Отправка двух файлов в телеграмм
                                    threading.Thread(target=run_async_code_in_thread, args=(FILE_TO_TELEGRAM,)).start()

                                graph_menu.update_log_display()


                            else:
                                debank.pasring_lucky_draw_in_txt_file(input_field_posts)
                                # завершаем поток
                                graph_menu.stop_thread_parsing = 'True'

                        elif name_action == 'debank_check':
                            debank = DebankActions(browser, 'metamask_wallet', public_key, browser_type)
                            debank.check_winner_lucky_draw(file_name_for_join_draw)

                        elif name_action == 'debank_voiting':
                            debank = DebankActions(browser, 'metamask_wallet', public_key, browser_type)

                            #metamask_wallet.connect_wallet_to_site(URL_DEBANK, 'Log in via web3 wallet', 'metamask')

                            debank.join_lucky_draw(file_name_for_join_draw, profile_id,progress_bar)

                        # Удаление подписчкиков
                        elif name_action == 'delete_followers':
                            debank = DebankActions(browser, 'metamask_wallet', public_key, browser_type)
                            debank.unfollow_followers(15, profile_id,progress_bar)
                        # Голосуем на спепшоте в выбранных проектах
                        elif name_action == 'snapshot':
                            snapshot = SnapshotVote(browser, profile_id, metamask_wallet,
                                                    public_key, root_dir, snap_project_name)
                            metamask_wallet.connect_wallet_to_site(URL_SNAPSHOT, 'connect', 'metamask')
                            snapshot.voiting()
                            graph_menu.stop_thread_parsing = 'True'

                        elif name_action == 'free':
                            free_activities = Free_activities(browser, metamask_wallet, public_key)

                            for activity in selecter_free_activities:
                                if activity == 'de.fi':
                                    free_activities.get_defi_daily_rewards()
                                    graph_menu.stop_thread_parsing = 'True'

                                elif activity == 'magiceden':
                                    free_activities.magic_eden_dayly_rewards()
                                elif activity == 'magicstore':
                                    free_activities.magic_store_dayly_rewards()
                                elif activity == 'nahmi':
                                    free_activities.nahmi_nft()
                                elif activity == 'parsing twitter':
                                    free_activities.parsing_twitter()


                        elif name_action == 'dmail':

                            dmail = Dmail(metamask_wallet, browser, profile_id, public_key)
                            # для каждоый из выбранной сети отправляем письмо !
                            for chain in selectet_chan_for_dmail:
                                # metamask_wallet.change_chain_in_metamask(chain)
                                dmail.send_letter(chain)

                            graph_menu.stop_thread_parsing = 'True'

                        # после закрываем профиль долфина
                        antybrowseraccount.close_profile_and_exit()

                        # time.sleep(random.uniform(4, 7))

                        # # имя сети с которой будем работать
                        # current_chain = ChainName.ZkSynk
                        #
                        # # получаем баланс кошелька в заданной сети
                        # start_balance, symbol, nonce = get_wallet_balance(public_key,
                        #                                                   current_chain)
                        #
                        # trx = TransactionWork(browser, public_key)
                        # trx_hash = trx.get_last_transaction(current_chain)
                        # if trx_hash != 0:
                        #     get_trx_attribute_transaction(current_chain, trx_hash)
                        # else:
                        #     logging.info(f'На кошельке не обнаружено ни одной транзакции в сети {ChainName.ZkSynk}')
                        #
                        # если баланс 0 то смысла продолжать нет
                        #
                        # step = 0.001
                        # if start_balance != 12:
                        #     print('Balance : ' + str(start_balance) + " " + symbol)
                        #     print(float(round(start_balance, 6)) * MIX_PERCENTAGE_OF_BALACE)
                        #     swap_amount = str(round(random.uniform(float(start_balance) * MIX_PERCENTAGE_OF_BALACE,
                        #                                            float(
                        #                                                start_balance) * MAX_PERCENTAGE_OF_BALACE),
                        #                             6))
                        #
                        #     print(f'swpa_ammount {swap_amount}')
                        #
                        #
                        # меняем сеть на ту с которой будем работать
                        # metamask_wallet.change_chain_in_metamask(current_chain)
                        # класс для работы с SyncSwap
                        # syncswap = SyncswapWork(browser, metamask_wallet, public_key)
                        # syncswap.connect_wallet()
                        # syncswap.swap_eth_to_usdc(TokenName.ETHEREUM, TokenName.UDSD, swap_amount)
                        # print('ждем следующего действвия')
                        # time.sleep(5)
                        # syncswap.connect_wallet()
                        # syncswap.swap_from_token_resiev_to_token_transmit(TokenName.UDSD, TokenName.ETHEREUM,
                        #                                                   swap_amount)
                        #
                        # spasefi = SpaseFiWork(browser, metamask_wallet, public_key)
                        # spasefi.connect_wallet()
                        # spasefi.swap_from_token_resiev_to_token_transmit(TokenName.ETHEREUM, TokenName.UDSD,
                        #                                                  swap_amount)
                        #
                        # maverik = MaverikWork(browser, metamask_wallet, public_key)
                        # maverik.connect_wallet()
                        # maverik.swap_from_token_resiev_to_token_transmit(TokenName.ETHEREUM, TokenName.MAV,
                        #                                                  swap_amount)
                        #
                        # debank.pasring_lucky_draw_in_txt_file(50)
                        # time.sleep(5)
                        # debank.sorting_lucky_draw('30')
                        # debank.join_lucky_draw()
                        #
                        # #############
                        # snapshot = SnapshotVote(browser, profile_id, metamask_wallet,
                        #                         public_key, root_dir, SNAPSHOT_MAGICAPP)
                        # metamask_wallet.connect_wallet_to_site(URL_SNAPSHOT, 'connect', 'metamask')
                        # snapshot.voiting()
                        # #############
                        #
                        # metamask_wallet.change_chain_in_metamask(ChainName.ZkSynk)
                        #
                        # metamask_wallet.connect_wallet_to_site('https://mail.dmail.ai/compose', 'metamask', '')
                        #
                        # dmail = Dmail(metamask_wallet, browser, profile_id, public_key)
                        # dmail.send_letter(ChainName.ZkSynk)
                        #
                        # else:
                        #     print(f'Баланс кошелька в сети {current_chain} = {start_balance} {symbol}')
                        #     # закрываем профиль
                        #     antybrowseraccount.close_profile_and_exit()
                        #     exit()



                else:
                    print(f'Error: browser is not start, close profile...')
                    antybrowseraccount.close_profile_and_exit()
                # exit()

        else:
            logging.info('Gas price is high..' + CANCEL)
            graph_menu.update_log_display()  # показываем лог в окне
    else:
        logging.info('Текущий поток успешно закрыт..' + STR_DONE)
        graph_menu.update_log_display()  # показываем лог в окне
        # делаем активную элементы на вкладке
        graph_menu.enable_tab_elements(graph_menu.tab2)
        graph_menu.enable_tab_elements(graph_menu.tab3)

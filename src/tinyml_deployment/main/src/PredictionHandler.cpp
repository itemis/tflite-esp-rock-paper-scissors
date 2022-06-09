#include "PredictionHandler.h"
#include <stdio.h>
#include "ascii_art.h"

void PredictionHandler::Update(uint8_t player_move) {
           // AI makes a random play
    int rand_num = (rand() % 3) + 1;
    std::string ai_move;
    std::string winner;
    std::string player_move_str;
    
    if (rand_num == 1) ai_move = "paper";
    if (rand_num == 2) ai_move = "rock";
    if (rand_num == 3) ai_move = "scissors";
    std::cout << "---- ---- ---- ----\n";
    std::cout << "AI plays: " << ai_move << "!\n";

    if (player_move == 0) {
        player_move_str = "paper";
        print_ascii_paper();
    }
    if (player_move == 1) {
        player_move_str = "rock";
        print_ascii_rock();
    }
    if (player_move == 2) {
        player_move_str = "scissors";
        print_ascii_scissors();
    }
    std::cout << "You play: " << player_move_str << "!\n";
    
    switch (player_move) {
            case 0: // paper
                if (ai_move == "rock") winner = "you";
                if (ai_move == "scissors") winner = "AI";
                if (ai_move == "paper") winner = "nobody! It's a draw!";
                break;
            case 1: // rock
                if (ai_move == "paper") winner = "AI";
                if (ai_move == "scissors") winner = "you";
                if (ai_move == "rock") winner = "nobody! It's a draw!";
                break;
            case 2: // scissors
                if (ai_move == "paper") winner = "you";
                if (ai_move == "rock") winner = "AI";
                if (ai_move == "scissors") winner = "nobody! It's a draw!";
                break;
            default:
                break;
        }

    std::cout << "The winner is " << winner << ".\n";
    std::cout << "---- ---- ---- ----\n";
    std::cout << "Cover the camera to start the next round.\n";   
    std::cout << "Waiting ...\n";
}

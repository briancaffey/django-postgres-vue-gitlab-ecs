/* eslint-disable promise/param-names, no-unused-vars */
import Vue from 'vue';
import { CHAT_GET_OR_CREATE_ROOM, CHAT_GET_MESSAGE } from '../actions/chat';


const state = {
  publicRooms: {},
};

const getters = {
  messages: s => {
    return roomName => state.publicRooms[roomName].messages;
  },
  sender: s => {
    return roomName => state.publicRooms[roomName].sender;
  }
};

const actions = {};

const mutations = {
  [CHAT_GET_OR_CREATE_ROOM]: (chatState, payload) => {
    const keys = Object.keys(chatState.publicRooms);
    if (keys.filter(x => x === payload.roomName).length === 0){
      Vue.set(
        chatState.publicRooms,
        payload.roomName,
        {'messages': [], 'sender': payload.sender, 'current': ''});
    }
  },
  [CHAT_GET_MESSAGE]: (chatState, payload) => {
    chatState.publicRooms[payload.roomName].messages.push(payload.message);
  }
};

export default {
  state,
  getters,
  actions,
  mutations,
};
